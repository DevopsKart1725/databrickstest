// This template is used to assign RBAC roles to the a Storage Account
targetScope = 'resourceGroup'

// Parameters
param storageAccountName string
param principalId string
param principalType string
param roleAssignments array = [
  //  {
  //    "roleName": "",
  //    "id": ""
  //  }
  ]

//Variables

// Resources
resource storageAccount 'Microsoft.Storage/storageAccounts@2021-09-01' existing = {
  name: storageAccountName
}

resource storageAccountRoleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = [for ra in roleAssignments: if (!empty(ra.id)) { 
  name: guid(uniqueString(storageAccount.id, principalId, ra.id))
  scope: storageAccount
  properties: {
    principalId: principalId
    principalType: principalType
    roleDefinitionId: resourceId('Microsoft.Authorization/roleDefinitions', ra.id)
  }
}]
