// This template is used to assign RBAC roles to a Azure Key Vault
targetScope = 'resourceGroup'

// Parameters
param keyVaultName string
param roleAssignments array = [
  // {
  //   principalId: ''
  //   role: ''
  //  }
 ]

//Variables
var roles = {
  'Key Vault Secrets User': '4633458b-17de-408a-b874-0445c86b69e6'
}

// Resources
resource keyVault 'Microsoft.KeyVault/vaults@2021-11-01-preview' existing = {
  name: keyVaultName
}

resource keyVaultRoleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = [for assignment in roleAssignments: if (!empty(assignment.principalId)) { 
  name: guid(keyVaultName, assignment.principalId)
  scope: keyVault
  properties: {
    principalId: assignment.principalId
    roleDefinitionId: resourceId('Microsoft.Authorization/roleDefinitions', roles[assignment.role])
  }
}]
