// This template is used to assign RBAC roles to a Azure Machine Learning
targetScope = 'resourceGroup'

// Parameters
param datafactoryName string
param roleAssignments array = [
  // {
  //   principalId: ''
  //   role: ''
  //  }
 ]

//Variables
var roles = {
  'Data Factory Contributor': '673868aa-7521-48a0-acc6-0f60742d39f5'
}

//Resources

resource dataFactory 'Microsoft.DataFactory/factories@2018-06-01' existing = {
  name: datafactoryName
}

resource adfRoleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = [for assignment in roleAssignments: if (!empty(assignment.principalId)) { 
  name: guid(dataFactory.id, assignment.principalId)
  scope: dataFactory
  properties: {
    principalId: assignment.principalId
    roleDefinitionId: resourceId('Microsoft.Authorization/roleDefinitions', roles[assignment.role])
  }
}]
