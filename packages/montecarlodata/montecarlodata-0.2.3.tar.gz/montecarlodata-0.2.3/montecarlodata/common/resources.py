import json
import secrets
import time
from typing import Optional, Dict

import click

from montecarlodata.common.user import UserService
from montecarlodata.config import Config
from montecarlodata.errors import complain_and_abort, manage_errors
from montecarlodata.utils import AwsClientWrapper


class CloudResourceService:
    _MCD_ROLE_PREFIX = 'monte-carlo-integration-role'
    _MCD_POLICY_PREFIX = 'monte-carlo-integration-cli-policy'
    _MCD_TAGS = [{'Key': 'MonteCarloData', 'Value': ''}]

    def __init__(self, config: Config, user_service: Optional[UserService] = None,
                 aws_wrapper: Optional[AwsClientWrapper] = None, aws_profile_override: Optional[str] = None):

        self._abort_on_error = True

        self._user_service = user_service or UserService(config=config)
        self._aws_wrapper = aws_wrapper or AwsClientWrapper(profile_name=aws_profile_override or config.aws_profile,
                                                            region_name=config.aws_region)

    @manage_errors
    def create_role(self, path_to_policy_doc: str) -> None:
        """
        Creates a DC compatible role from the provided policy doc
        """
        current_time = str(time.time())
        external_id = self._generate_random_token()
        role_name = f'{self._MCD_ROLE_PREFIX}-{current_time}'
        policy_name = f'{self._MCD_POLICY_PREFIX}-{current_time}'

        try:
            policy = json.dumps(self._read_json(path_to_policy_doc))

            # use the AWS account id of collector, which may not necessarily be account id running the CLI
            account_id = self._user_service.active_collector['customerAwsAccountId']
        except json.decoder.JSONDecodeError as err:
            complain_and_abort(f'The provided policy is not valid JSON - {err}')
        except KeyError as err:
            complain_and_abort(f'Missing expected property ({err}). The collector may not have been deployed before')
        else:
            trust_policy = self._generate_trust_policy(account_id=account_id, external_id=external_id)
            role_arn = self._aws_wrapper.create_role(role_name=role_name, trust_policy=trust_policy, tags=self._MCD_TAGS)
            click.echo(f"Created role with ARN - '{role_arn}' and external id - '{external_id}'.")

            self._aws_wrapper.attach_inline_policy(role_name=role_name, policy_name=policy_name, policy_doc=policy)
            click.echo(f'Success! Attached provided policy.')

    @staticmethod
    def _generate_trust_policy(account_id: str, external_id: str) -> str:
        """
        Generates a DC compatible trust policy
        """
        return json.dumps(
            {
                'Version': '2012-10-17',
                'Statement': [
                    {
                        'Effect': 'Allow',
                        'Principal': {
                            'AWS': f'arn:aws:iam::{account_id}:root'
                        },
                        'Action': 'sts:AssumeRole',
                        'Condition': {
                            'StringEquals': {
                                'sts:ExternalId': external_id
                            }
                        }
                    }
                ]
            }
        )

    @staticmethod
    def _generate_random_token(length: Optional[int] = 16) -> str:
        """
        Generates a random token (e.g. for the external id)
        """
        return secrets.token_urlsafe(length)

    @staticmethod
    def _read_json(path: str) -> Dict:
        """
        Reads a JSON file from the path.
        """
        with open(path) as file:
            return json.load(file)  # loads for the purpose of validating
