# Queries related to managing the collector

GENERATE_COLLECTOR_TEMPLATE = """
mutation generateCollectorTemplate {
  generateCollectorTemplate {
    dc {
      templateLaunchUrl
      stackArn
      customerAwsAccountId
      active
      apiGatewayId
    }
  }
}
"""
