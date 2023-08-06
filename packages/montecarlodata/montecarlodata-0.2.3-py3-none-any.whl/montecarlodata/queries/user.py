# Queries related to users

GET_USER_QUERY = """
query getUser {
  getUser {
    firstName
    lastName
    account {
      uuid
      dataCollectors {
        uuid
        stackArn
        active
        customerAwsAccountId
        warehouses {
          uuid
          connections {
            uuid
            type
            createdOn
            jobTypes
          }
        }
      }
    }
  }
}
"""
