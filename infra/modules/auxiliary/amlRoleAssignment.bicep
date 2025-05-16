// This template is used to assign RBAC roles to a Azure Machine Learning
targetScope = 'resourceGroup'

// Parameters
param machineLearningName string
param roleAssignments array = [
  // {
  //   principalId: ''
  //   role: ''
  //  }
 ]

//Variables
var roles = {
  'Contributor': 'b24988ac-6180-42a0-ab88-20f7382dd24c'
  'AzureML Data Scientist': 'f6c7c914-8db3-469d-8ca1-694a8f32e121'
}

//Resources

resource machineLearning 'Microsoft.MachineLearningServices/workspaces@2022-05-01' existing = {
  name: machineLearningName
}

resource amlRoleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = [for assignment in roleAssignments: if (!empty(assignment.principalId)) { 
  name: guid(machineLearning.id, assignment.principalId)
  scope: machineLearning
  properties: {
    principalId: assignment.principalId
    roleDefinitionId: resourceId('Microsoft.Authorization/roleDefinitions', roles[assignment.role])
  }
}]
