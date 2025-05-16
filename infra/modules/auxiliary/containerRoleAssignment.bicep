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
var storageAccountFileSystemName = length(split(storageAccountFileSystemId, '/')) >= 13 ? last(split(storageAccountFileSystemId, '/')) : 'incorrectSegmentLength'
var storageAccountName = length(split(storageAccountFileSystemId, '/')) >= 13 ? split(storageAccountFileSystemId, '/')[8] : 'incorrectSegmentLength'

// Resources
resource storageAccountFileSystem 'Microsoft.Storage/storageAccounts/blobServices/containers@2021-02-01' existing = {
  name: '${storageAccountName}/default/${storageAccountFileSystemName}'
}

var roles = {
  'Storage Blob Data Contributor': 'ba92f5b4-2d11-453d-a403-e96b0029c9fe'
  'Storage Blob Data Reader': '2a2b9908-6ea1-4ae2-8e65-a410df84e7d1'
}


resource containerRoleAssignment 'Microsoft.Authorization/roleAssignments@2020-04-01-preview' = [for assignment in roleAssignments: if (!empty(assignment.principalId)) { 
  name: guid(storageAccountFileSystem.id,assignment.principalId)
  scope: storageAccountFileSystem
  properties: {
    roleDefinitionId: resourceId('Microsoft.Authorization/roleDefinitions', roles[assignment.role])
    principalId: assignment.principalId
  }
}]


