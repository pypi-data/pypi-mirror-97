# Queries related to onboarding

TEST_PRESTO_CRED_MUTATION = """
mutation testPrestoCredentials($catalog:String, $host:String, $httpScheme:String, $password:String, $port:Int, $schema:String, $sslOptions:SslInputOptions, $user:String) {
  testPrestoCredentials(catalog:$catalog, host:$host, httpScheme:$httpScheme, password:$password, port:$port, schema:$schema, sslOptions: $sslOptions, user:$user) {
    key
  }
}
"""

TEST_S3_CRED_MUTATION = """
mutation tests3Credentials($bucket:String, $prefix:String, $assumableRole:String, $externalId:String, $connectionType:String) {
  testS3Credentials(bucket:$bucket, prefix:$prefix, assumableRole:$assumableRole, externalId:$externalId, connectionType:$connectionType) {
    key
  }
}
"""

TEST_DATABASE_CRED_MUTATION = """
mutation testDatabaseCredentials($assumableRole:String, $connectionType:String, $dbName:String, $externalId:String, $host:String, $password:String, $port:Int, $sslOptions:SslInputOptions, $user:String) {
  testDatabaseCredentials(assumableRole:$assumableRole, connectionType:$connectionType, dbName:$dbName, externalId:$externalId, host:$host, password:$password, port:$port, sslOptions:$sslOptions, user:$user) {
    key
  }
}
"""

TEST_HIVE_SQL_CRED_MUTATION = """
mutation testHiveCredentials($database:String, $host:String, $port:Int, $username:String) {
  testHiveCredentials(database:$database, host:$host, port:$port, username:$username) {
    key
    success
  }
}
"""

TEST_GLUE_CRED_MUTATION = """
mutation testGlueS3Credentials($assumableRole:String, $externalId:String) {
  testGlueS3Credentials(assumableRole:$assumableRole, externalId:$externalId) {
    key
  }
}
"""

TEST_ATHENA_CRED_MUTATION = """
mutation testAthenaCredentials($assumableRole:String, $catalog:String, $externalId:String, $workgroup:String) {
  testAthenaCredentials(assumableRole:$assumableRole, catalog:$catalog, externalId:$externalId, workgroup:$workgroup) {
    key
  }
}
"""

TEST_SPARK_BINARY_MODE_CRED_MUTATION = """
mutation testSparkCredentials($database:String!, $host:String!, $port:Int!, $username:String!, $password:String!) {
  testSparkCredentials(binaryMode: {database:$database, host:$host, port:$port, username:$username, password:$password}) {
    key
  }
}
"""

TEST_SPARK_HTTP_MODE_CRED_MUTATION = """
mutation testSparkCredentials($url:String!, $username:String!, $password:String!) {
  testSparkCredentials(httpMode: {url:$url, username:$username, password:$password}) {
    key
  }
}
"""

TEST_SPARK_DATABRICKS_CRED_MUTATION = """
mutation testSparkCredentials($workspaceUrl:String!, $workspaceId:String!, $clusterId:String!, $token:String!) {
  testSparkCredentials(databricks: {workspaceUrl:$workspaceUrl, workspaceId:$workspaceId, clusterId:$clusterId, token:$token}) {
    key
  }
}
"""

TOGGLE_METADATA_EVENT_MUTATION = """
mutation toggleEventMetadataConfig($dwId:UUID!, $enable:Boolean!, $connectionType:String!) {
  toggleEventConfig(dwId:$dwId, enable:$enable, connectionType:$connectionType, eventType: s3_metadata_events){
    success
  }
}
"""

ADD_CONNECTION_MUTATION = """
mutation addConnection($connectionType:String!, $createWarehouseType:String, $dwId:UUID, $jobTypes:[String], $key:String!, $jobLimits:JSONString) {
  addConnection(connectionType:$connectionType, createWarehouseType:$createWarehouseType, dwId:$dwId, jobTypes:$jobTypes, key:$key, jobLimits:$jobLimits){
    connection {
      uuid
    }
  }
}
"""
