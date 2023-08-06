import click
import click_config_file

import montecarlodata.settings as settings
from montecarlodata.common.resources import CloudResourceService
from montecarlodata.errors import complain_and_abort
from montecarlodata.integrations.info.status import OnboardingStatusService
from montecarlodata.integrations.onboarding.data_lake.events import EventsOnboardingService
from montecarlodata.integrations.onboarding.data_lake.glue_athena import GlueAthenaOnboardingService
from montecarlodata.integrations.onboarding.data_lake.hive import HiveOnboardingService
from montecarlodata.integrations.onboarding.data_lake.presto import PrestoOnboardingService
from montecarlodata.integrations.onboarding.data_lake.spark import SparkOnboardingService,\
    SPARK_HTTP_MODE_CONFIG_TYPE, SPARK_DATABRICKS_CONFIG_TYPE, SPARK_BINARY_MODE_CONFIG_TYPE
from montecarlodata.integrations.onboarding.fields import HIVE_MYSQL_CONNECTION_TYPE, GLUE_CONNECTION_TYPE
from montecarlodata.tools import add_common_options

# Options shared across commands
ROLE_OPTIONS = [
    click.option('--role', help='Assumable role ARN to use for accessing AWS resources.', required=False),
    click.option('--external-id', help='An external id, per assumable role conditions.', required=False),
]
S3_OPTIONS = [
    click.option('--bucket', help='S3 Bucket where query logs are contained.', required=True),
    click.option('--prefix', help='Path to query logs.', required=True),
    *ROLE_OPTIONS
]
EVENT_OPTIONS = [
    click.option('--enable/--disable', 'toggle', help='Enable or disable events. Enables if not specified.',
                 default=True)
]

# Shared command verbiage
METADATA_VERBIAGE = 'For metadata'
QL_VERBIAGE = 'For query logs'
SQL_VERBIAGE = 'For health queries'
EVENT_VERBIAGE = 'For tracking data freshness and volume at scale. Requires s3 notifications to be configured first'


@click.group(help='Manage or integrate an asset with Monte Carlo.')
def integrations():
    """
    Group for any integration related subcommands
    """
    pass


@integrations.command(help=f'Setup a Hive metastore integration (MySQL). {METADATA_VERBIAGE}.')
@click.pass_obj
@click.option('--host', help='Hostname.', required=True)
@click.option('--port', help='HTTP port.', default=3306, type=click.INT, show_default=True)
@click.option('--user', help='Username with access to the metastore.', required=False)
@click.password_option('--password', help='User\'s password.', prompt='Password for user', required=True)
@click.option('--database', help='Name of database for the metastore.', required=True)
@click.option('--use-ssl', help='Use SSL to connect (using AWS RDS certificates).', required=False, is_flag=True,
              default=False, show_default=True)
@click.option('--catalog', help='Presto catalog name. For using multiple hive clusters with Presto. '
                                'Uses \'hive\' if not specified.', required=False)
@click_config_file.configuration_option(settings.OPTION_FILE_FLAG)
def add_hive_metastore(ctx, host, port, user, password, database, use_ssl, catalog):
    """
    Onboard a hive metastore connection (MySQL)
    """
    HiveOnboardingService(config=ctx['config']).onboard_hive_mysql(host=host, port=port, user=user, password=password,
                                                                   dbName=database, use_ssl=use_ssl, catalog=catalog)


@integrations.command(help=f'Setup a Presto SQL integration. {SQL_VERBIAGE}.')
@click.pass_obj
@click.option('--host', help='Hostname.', required=True)
@click.option('--port', help='HTTP port.', default=8889, type=click.INT, show_default=True)
@click.option('--user', help='Username with access to catalog/schema.', required=False)
@click.password_option('--password', help='User\'s password.', prompt='Password for user (enter to skip)',
                       default='', required=False)
@click.option('--catalog', help='Mount point to access data source.', required=True)
@click.option('--schema', help='Schema to access.', required=True)
@click.option('--http-scheme', help='Scheme for authentication.',
              type=click.Choice(['http', 'https'], case_sensitive=True), required=True)
@click.option('--cert-file', help='Local SSL certificate file to upload to collector.', required=False,
              type=click.Path(dir_okay=False, exists=True))
@click.option('--cert-s3', help='Object path (key) to a certificate already uploaded to the collector.',
              required=False)
@click_config_file.configuration_option(settings.OPTION_FILE_FLAG)
def add_presto(ctx, host, port, user, password, catalog, schema, http_scheme, cert_file, cert_s3):
    """
    Onboard a presto sql connection
    """
    if not password:
        password = None  # make explicitly null if not set. Prompts can't be None
    if cert_file is not None and cert_s3 is not None:
        complain_and_abort('Can have a cert-file or cert-s3-path, but not both')
    PrestoOnboardingService(config=ctx['config']).onboard_presto_sql(host=host, port=port, user=user, password=password,
                                                                     catalog=catalog, schema=schema,
                                                                     http_scheme=http_scheme, cert_file=cert_file,
                                                                     cert_s3=cert_s3)


@integrations.command(help=f'Setup a Hive SQL integration. {SQL_VERBIAGE}.')
@click.pass_obj
@click.option('--host', help='Hostname.', required=True)
@click.option('--database', help='Name of database.', required=False)
@click.option('--port', help='HTTP port.', default=10000, type=click.INT, show_default=True)
@click.option('--user', help='Username with access to hive.', required=True)
@click_config_file.configuration_option(settings.OPTION_FILE_FLAG)
def add_hive(ctx, host, database, port, user):
    HiveOnboardingService(config=ctx['config']).onboard_hive_sql(host=host, database=database, port=port, username=user)


@integrations.command(help=f'Setup a Presto logs integration (S3). {QL_VERBIAGE}.')
@click.pass_obj
@add_common_options(S3_OPTIONS)
@click_config_file.configuration_option(settings.OPTION_FILE_FLAG)
def add_presto_logs(ctx, bucket, prefix, role, external_id):
    """
    Onboard a presto logs (s3) connection
    """
    PrestoOnboardingService(config=ctx['config']).onboard_presto_s3(bucket=bucket, prefix=prefix,
                                                                    assumable_role=role, external_id=external_id)


@integrations.command(help=f'Setup a Hive EMR logs integration (S3). {QL_VERBIAGE}.')
@click.pass_obj
@add_common_options(S3_OPTIONS)
@click_config_file.configuration_option(settings.OPTION_FILE_FLAG)
def add_hive_logs(ctx, bucket, prefix, role, external_id):
    """
    Onboard a hive emr (s3) connection
    """
    HiveOnboardingService(config=ctx['config']).onboard_hive_s3(bucket=bucket, prefix=prefix, assumable_role=role,
                                                                external_id=external_id)


@integrations.command(help=f'Setup a Glue integration. {METADATA_VERBIAGE}.')
@click.pass_obj
@add_common_options(ROLE_OPTIONS)
@click_config_file.configuration_option(settings.OPTION_FILE_FLAG)
def add_glue(ctx, role, external_id):
    """
    Onboard a glue connection
    """
    GlueAthenaOnboardingService(config=ctx['config']).onboard_glue(assumable_role=role, external_id=external_id)


@integrations.command(help=f'Setup an Athena integration. For query logs and health queries.')
@click.pass_obj
@click.option('--catalog', help='Glue data catalog. If not specified the AwsDataCatalog is used.', required=False)
@click.option('--workgroup',
              help='Workbook for running queries and retrieving logs. If not specified the primary is used.',
              required=False)
@add_common_options(ROLE_OPTIONS)
@click_config_file.configuration_option(settings.OPTION_FILE_FLAG)
def add_athena(ctx, catalog, workgroup, role, external_id):
    """
    Onboard an athena connection
    """
    GlueAthenaOnboardingService(config=ctx['config']).onboard_athena(catalog=catalog, workgroup=workgroup,
                                                                     assumable_role=role, external_id=external_id)


@integrations.command(help=f'Setup a Spark integration in Thrift binary mode. {SQL_VERBIAGE}.')
@click.pass_obj
@click.option('--host', help='Hostname.', required=True)
@click.option('--database', help='Name of database.', required=True)
@click.option('--port', help='Port.', default=10000, type=click.INT, show_default=True)
@click.option('--user', help='Username with access to spark.', required=True)
@click.password_option('--password', help='User\'s password.', prompt='Password for user', required=True)
@click_config_file.configuration_option(settings.OPTION_FILE_FLAG)
def add_spark_binary_mode(ctx, host, database, port, user, password):
    """
    Onboard a spark connection, thrift binary mode
    """
    SparkOnboardingService(config=ctx['config']).onboard_spark(SPARK_BINARY_MODE_CONFIG_TYPE,
                                                               host=host, database=database, port=port, username=user,
                                                               password=password)


@integrations.command(help=f'Setup a Spark integration in Thrift HTTP mode. {SQL_VERBIAGE}.')
@click.pass_obj
@click.option('--url', help='HTTP URL.', required=True)
@click.option('--user', help='Username with access to spark.', required=True)
@click.password_option('--password', help='User\'s password.', prompt='Password for user', required=True)
@click_config_file.configuration_option(settings.OPTION_FILE_FLAG)
def add_spark_http_mode(ctx, url, user, password):
    """
    Onboard a spark connection, thrift http mode
    """
    SparkOnboardingService(config=ctx['config']).onboard_spark(SPARK_HTTP_MODE_CONFIG_TYPE,
                                                               url=url, username=user, password=password)


@integrations.command(help=f'Setup a Spark integration for Databricks. {SQL_VERBIAGE}.')
@click.pass_obj
@click.option('--workspace-url', help='Databricks workspace URL.', required=True)
@click.option('--workspace-id', help='Databricks workspace ID.', required=True)
@click.option('--cluster-id', help='Databricks cluster ID.', required=True)
@click.password_option('--token', help='Databricks access token.', prompt='Databricks access token', required=True)
@click_config_file.configuration_option(settings.OPTION_FILE_FLAG)
def add_spark_databricks(ctx, workspace_url, workspace_id, cluster_id, token):
    """
    Onboard a spark connection, databricks
    """
    SparkOnboardingService(config=ctx['config']).onboard_spark(SPARK_DATABRICKS_CONFIG_TYPE,
                                                               workspace_url=workspace_url, workspace_id=workspace_id,
                                                               cluster_id=cluster_id, token=token)


@integrations.command(help=f'Toggle S3 events for a Hive/Presto lake. {EVENT_VERBIAGE}.')
@click.pass_obj
@add_common_options(EVENT_OPTIONS)
@click_config_file.configuration_option(settings.OPTION_FILE_FLAG)
def toggle_hive_events(ctx, toggle):
    """
    Toggle s3 events for a hive lake
    """
    EventsOnboardingService(config=ctx['config']).toggle_event_configuration(enable=toggle,
                                                                             connectionType=HIVE_MYSQL_CONNECTION_TYPE)


@integrations.command(help=f'Toggle S3 events for a Glue/Athena lake. {EVENT_VERBIAGE}.')
@click.pass_obj
@add_common_options(EVENT_OPTIONS)
@click_config_file.configuration_option(settings.OPTION_FILE_FLAG)
def toggle_glue_events(ctx, toggle):
    """
    Toggle s3 events for a glue lake
    """
    EventsOnboardingService(config=ctx['config']).toggle_event_configuration(enable=toggle,
                                                                             connectionType=GLUE_CONNECTION_TYPE)


@integrations.command(help=f'List all active integrations.', name='list')
@click.pass_obj
@click_config_file.configuration_option(settings.OPTION_FILE_FLAG)
def display_integrations(ctx):
    """
    Display active integrations
    """
    OnboardingStatusService(config=ctx['config']).display_integrations()


@integrations.command(help='Create an IAM role from the provided policy FILE. '
                           'The returned role ARN and external id should be used for adding lake assets.')
@click.pass_obj
@click.argument('file', type=click.Path(dir_okay=False, exists=True))
@click.option('--aws-profile', required=False,
              help='Override the AWS profile used by the CLI, which determines where the role is created. '
                   'This can be helpful when the account that manages the asset is not the same as the collector.')
def create_role(ctx, file, aws_profile):
    """
    Create a collector compatible role from the provided policy
    """
    CloudResourceService(config=ctx['config'], aws_profile_override=aws_profile).create_role(path_to_policy_doc=file)
