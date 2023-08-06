import json
import os
from typing import Optional, Dict, List

import click

from montecarlodata.common.user import UserService
from montecarlodata.config import Config
from montecarlodata.errors import complain_and_abort
from montecarlodata.integrations.onboarding.fields import S3_CERT_MECHANISM, GQL_TO_FRIENDLY_CONNECTION_MAP
from montecarlodata.queries.onboarding import ADD_CONNECTION_MUTATION
from montecarlodata.utils import GqlWrapper, AwsClientWrapper


class BaseOnboardingService:

    def __init__(self, config: Config, user_service: Optional[UserService] = None,
                 request_wrapper: Optional[GqlWrapper] = None,
                 aws_wrapper: Optional[AwsClientWrapper] = None):

        self._abort_on_error = True  # Aborts methods with deco on unhandled error
        self._dc_outputs = None

        self._user_service = user_service or UserService(config=config)
        self._request_wrapper = request_wrapper or GqlWrapper(mcd_id=config.mcd_id, mcd_token=config.mcd_token)
        self._aws_wrapper = aws_wrapper or AwsClientWrapper(profile_name=config.aws_profile,
                                                            region_name=config.aws_region)

    def onboard(self, validation_query: str, validation_response: str, connection_type: str,
                job_types: Optional[List[str]] = None, job_limits: Optional[Dict] = None, **kwargs):
        """
        Convenience wrapper to validate and add a connection.
        """
        temp_path = self._validate_connection(query=validation_query, response_field=validation_response, **kwargs)
        self._add_connection(temp_path=temp_path, connection_type=connection_type, job_types=job_types,
                             job_limits=job_limits)

    def handle_cert(self, cert_prefix: str, options: Dict) -> None:
        """
        Handles cert payload from either an s3 path or file. Uploading the latter
        Options is updated if successful.
        """
        if options.get('cert_file') is not None:
            bucket_name = self._get_dc_property(prop='PrivateS3BucketArn').split(':')[5]  # get name from arn
            object_name = os.path.join(cert_prefix, os.path.basename(options['cert_file']))
            self._aws_wrapper.upload_file(bucket_name=bucket_name, object_name=object_name,
                                          file_path=options['cert_file'])

            click.echo(f"Uploaded '{options['cert_file']}' to s3://{bucket_name}/{object_name}")
            options['cert_s3'] = object_name

        if options.get('cert_s3') is not None:
            # reformat to generic options and specify a mechanism
            options['ssl_options'] = {'mechanism': S3_CERT_MECHANISM, 'cert': options.pop('cert_s3')}
        options.pop('cert_file', None)

    def _validate_connection(self, query: str, response_field: str, **kwargs) -> str:
        """
        Validate connection before adding using the expected gql response_field (e.g. testPrestoCredentials)
        """
        variables = self._request_wrapper.convert_snakes_to_camels(kwargs)
        temp_path = self._request_wrapper.make_request(
            query=query, variables=variables).get(response_field, {}).get('key')

        if temp_path is not None:
            click.echo('Connection validated!')
            return temp_path
        complain_and_abort('Connection failed!')

    def _add_connection(self, temp_path: str, connection_type: str, job_types: Optional[List[str]] = None,
                        warehouse_type: Optional[str] = 'data-lake', job_limits: Optional[Dict] = None) -> bool:
        """
        Add connection and setup any associated jobs
        """
        connection_request = {'key': temp_path, 'connectionType': connection_type}
        num_of_warehouses = len(self._user_service.warehouses)

        # If no warehouse has been created for this account specify the type, otherwise pass the existing warehouse id
        if num_of_warehouses == 0:
            connection_request['createWarehouseType'] = warehouse_type
        elif num_of_warehouses == 1:
            connection_request['dwId'] = self._user_service.warehouses[0]['uuid']
        else:
            complain_and_abort('More than one warehouse is not supported')

        if job_types:
            # specify job types if set
            connection_request['jobTypes'] = job_types
        if job_limits:
            connection_request['jobLimits'] = json.dumps(job_limits)

        response = self._request_wrapper.make_request(query=ADD_CONNECTION_MUTATION, variables=connection_request)
        connection_id = response.get('addConnection', {}).get('connection', {}).get('uuid')
        if connection_id is not None:
            click.echo(f"Success! Added connection for "
                       f"{GQL_TO_FRIENDLY_CONNECTION_MAP.get(connection_type, connection_type.capitalize())}.")
            return True
        complain_and_abort('Failed to add connection!')

    def _get_dc_property(self, prop: str) -> Optional[str]:
        """
        Retrieve property from DC stack outputs
        """
        self._dc_outputs = self._dc_outputs or self._aws_wrapper.get_stack_outputs(
            self._user_service.active_collector['stackArn'])  # cache lookup
        for output in self._dc_outputs:
            if output['OutputKey'] == prop:
                return output['OutputValue']
