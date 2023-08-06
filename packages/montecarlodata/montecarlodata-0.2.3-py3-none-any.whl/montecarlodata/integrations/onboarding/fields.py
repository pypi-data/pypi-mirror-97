# Query responses
EXPECTED_HIVE_MYSQL_GQL_RESPONSE_FIELD = 'testDatabaseCredentials'
EXPECTED_HIVE_S3_GQL_RESPONSE_FIELD = 'testS3Credentials'
EXPECTED_HIVE_SQL_GQL_RESPONSE_FIELD = 'testHiveCredentials'
EXPECTED_PRESTO_SQL_GQL_RESPONSE_FIELD = 'testPrestoCredentials'
EXPECTED_PRESTO_S3_GQL_RESPONSE_FIELD = 'testS3Credentials'
EXPECTED_GLUE_GQL_RESPONSE_FIELD = 'testGlueS3Credentials'
EXPECTED_ATHENA_GQL_RESPONSE_FIELD = 'testAthenaCredentials'
EXPECTED_SPARK_GQL_RESPONSE_FIELD = 'testSparkCredentials'
EXPECTED_TOGGLE_EVENTS_GQL_RESPONSE_FIELD = 'toggleEventConfig'

# Available connections types
HIVE_MYSQL_CONNECTION_TYPE = 'hive-mysql'
HIVE_S3_CONNECTION_TYPE = 'hive-s3'
HIVE_SQL_CONNECTION_TYPE = 'hive'
PRESTO_SQL_CONNECTION_TYPE = 'presto'
PRESTO_S3_CONNECTION_TYPE = 'presto-s3'
GLUE_CONNECTION_TYPE = 'glue-s3'
ATHENA_CONNECTION_TYPE = 'athena'
SPARK_CONNECTION_TYPE = 'spark'

# Job types
QL_JOB_TYPE = ['query_logs']

# Job limits
PRESTO_CATALOG_KEY = 'catalog_name'

# Certificate details
S3_CERT_MECHANISM = 'dc-s3'
PRESTO_CERT_PREFIX = 'certificates/presto/'
AWS_RDS_CA_CERT = 'https://s3.amazonaws.com/rds-downloads/rds-combined-ca-bundle.pem'

# Connections to friendly name (i.e. human presentable) map
GQL_TO_FRIENDLY_CONNECTION_MAP = {
    HIVE_MYSQL_CONNECTION_TYPE: 'Hive (metastore)',
    HIVE_S3_CONNECTION_TYPE: 'Hive (EMR logs)',
    HIVE_SQL_CONNECTION_TYPE: 'Hive (SQL)',
    PRESTO_SQL_CONNECTION_TYPE: 'Presto',
    PRESTO_S3_CONNECTION_TYPE: 'Presto (logs)',
    GLUE_CONNECTION_TYPE: 'Glue',
    ATHENA_CONNECTION_TYPE: 'Athena',
    SPARK_CONNECTION_TYPE: 'Spark (SQL)',
}
