// Copyright (c) Microsoft Corporation.
// Licensed under the MIT license.

// The module contains a template to create a role assignment of the ADF to a storage file system.
targetScope = 'resourceGroup'

// Parameters
param storageAccountFileSystemId string
param roleAssignments array = [
  // {
  //   principalId: ''
  //   role: ''
  //  }
 ]

// Variables
var storageAccountName = length(split(storageAccountFileSystemId, '/')) >= 8 ? split(storageAccountFileSystemId, '/')[8] : 'incorrectSegmentLength'

// Resources
resource storageAccount'Microsoft.Storage/storageAccounts@2021-04-01' existing = {
  name: storageAccountName
}

var roles = {
  'Storage Blob Data Reader': '2a2b9908-6ea1-4ae2-8e65-a410df84e7d1'
}


resource storageRoleAssignment 'Microsoft.Authorization/roleAssignments@2020-04-01-preview' = [for assignment in roleAssignments: if (!empty(assignment.principalId)) { 
  name: guid(storageAccountName,assignment.principalId)
  scope: storageAccount
  properties: {
    roleDefinitionId: resourceId('Microsoft.Authorization/roleDefinitions', roles[assignment.role])
    principalId: assignment.principalId
  }
}]

