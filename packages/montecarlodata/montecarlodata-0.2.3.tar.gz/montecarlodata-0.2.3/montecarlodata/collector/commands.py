import click
import click_config_file

import montecarlodata.settings as settings
from montecarlodata.collector.management import CollectorManagementService
from montecarlodata.tools import validate_json_callback


@click.group(help='Manage the data collector.')
def collector():
    """
    Group for any collector related subcommands
    """
    pass


@collector.command(help='Get link to the latest template. For initial deployment or manually upgrading.')
@click.pass_obj
@click_config_file.configuration_option(settings.OPTION_FILE_FLAG)
def get_template(ctx):
    """
    Get the latest template for this account
    """
    CollectorManagementService(config=ctx['config']).echo_template()


@collector.command(help='Upgrade to the latest version.')
@click.pass_obj
@click.option('--params', required=False, default=None, callback=validate_json_callback,
              help="""
              Parameters key,value pairs as JSON. If a key is not specified the existing (or default) value is used.
              \b
              \n
              E.g. --params '{"CreateEventInfra":"True"}'
              """)  # \b disables wrapping
@click_config_file.configuration_option(settings.OPTION_FILE_FLAG)
def upgrade(ctx, params):
    """
    Upgrade the collector for this account
    """
    CollectorManagementService(config=ctx['config']).upgrade_template(new_params=params)
