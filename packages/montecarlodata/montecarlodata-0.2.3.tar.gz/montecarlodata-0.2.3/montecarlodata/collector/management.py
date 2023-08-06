import copy
from typing import Optional, Dict, List
from urllib import parse

import click

from montecarlodata.common.user import UserService
from montecarlodata.config import Config
from montecarlodata.errors import manage_errors, complain_and_abort
from montecarlodata.queries.collector import GENERATE_COLLECTOR_TEMPLATE
from montecarlodata.utils import GqlWrapper, AwsClientWrapper


class CollectorManagementService:
    def __init__(self, config: Config, user_service: Optional[UserService] = None,
                 request_wrapper: Optional[GqlWrapper] = None,
                 aws_wrapper: Optional[AwsClientWrapper] = None):
        self._abort_on_error = True

        self._user_service = user_service or UserService(config=config)
        self._request_wrapper = request_wrapper or GqlWrapper(mcd_id=config.mcd_id, mcd_token=config.mcd_token)
        self._aws_wrapper = aws_wrapper or AwsClientWrapper(profile_name=config.aws_profile,
                                                            region_name=config.aws_region)

    @manage_errors
    def echo_template(self) -> None:
        """
        Echos the most recent template for this account
        """
        click.echo(self._get_template_url_from_launch(self._generate_collector_template().get('templateLaunchUrl')))

    @manage_errors
    def upgrade_template(self, new_params: Optional[Dict] = None) -> None:
        """
        Upgrades the DC attached to this account
        """
        collector_details = self._generate_collector_template()
        try:
            stack_arn = collector_details['stackArn']
            is_active = collector_details['active']
            gateway_id = collector_details['apiGatewayId']
            template_url = self._get_template_url_from_launch(collector_details['templateLaunchUrl'])

            if not is_active:
                complain_and_abort('Cannot upgrade an inactive collector. Please contact Monte Carlo')
        except KeyError as err:
            complain_and_abort(f'Missing expected property ({err}). The collector may not have been deployed before')
        else:
            click.echo(f'Updating \'{stack_arn}\'')
            self._upgrade(stack_arn=stack_arn, template_url=template_url, gateway_id=gateway_id, new_params=new_params)
            click.echo('Upgrade complete! Have a nice day!')

    def _upgrade(self, stack_arn: str, template_url: str, gateway_id: str, new_params: Dict):
        """
        Upgrade the collector stack and deploy the gateway
        """
        parameters = self._build_param_list(self._aws_wrapper.get_stack_parameters(stack_id=stack_arn), new_params)
        if self._aws_wrapper.upgrade_stack(stack_id=stack_arn, template_link=template_url, parameters=parameters):
            self._aws_wrapper.deploy_gateway(gateway_id=gateway_id)
        else:
            complain_and_abort('Failed to upgrade. Please review CF events for details')

    def _generate_collector_template(self) -> Optional[Dict]:
        """
        Generate the latest template and returns any associated dc properties (i.e. from the DataCollectorModel)
        """
        response = self._request_wrapper.make_request(GENERATE_COLLECTOR_TEMPLATE)
        return response['generateCollectorTemplate'].get('dc')

    @staticmethod
    def _get_template_url_from_launch(launch_url: str) -> str:
        """
        Extract the template url from expected launch url structure
        """
        return parse.parse_qs(parse.urlparse(launch_url).fragment).get('templateURL', [])[0]

    @staticmethod
    def _build_param_list(existing_params: List[Dict], new_params: Optional[Dict] = None) -> List[Dict]:
        """
        Get a list of parameters by replacing (or extending) any new params into the existing stack params
        """
        existing_params = copy.deepcopy(existing_params)
        new_params = copy.deepcopy(new_params)

        for param in existing_params or []:
            if new_params and new_params.get(param['ParameterKey']) is not None:
                param['ParameterValue'] = new_params[param['ParameterKey']]
                param['UsePreviousValue'] = False
                del new_params[param['ParameterKey']]
            else:
                del param['ParameterValue']
                param['UsePreviousValue'] = True
        if new_params:
            # Handle any completely new params (i.e. those that were not in the existing struct)
            # Can be found for params added between versions
            existing_params.extend([{'ParameterKey': k, 'ParameterValue': v} for k, v in new_params.items()])

        return existing_params
