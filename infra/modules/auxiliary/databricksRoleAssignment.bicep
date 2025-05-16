// This template is used to assign RBAC roles to a Databricks
targetScope = 'resourceGroup'

// Parameters
param databricksName string
param roleAssignments array = [

]

//Variables
var roles = {
  Contributor: 'b24988ac-6180-42a0-ab88-20f7382dd24c'
}

//Resources

resource databricks 'Microsoft.Databricks/workspaces@2021-04-01-preview' existing = {
  name: databricksName
}

resource databricksRoleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = [for assignment in roleAssignments: if (!empty(assignment.principalId)) { 
  name: guid(databricks.id, assignment.principalId)
  scope: databricks
  properties: {
    principalId: assignment.principalId
    roleDefinitionId: resourceId('Microsoft.Authorization/roleDefinitions', roles[assignment.role])
  }
}]
