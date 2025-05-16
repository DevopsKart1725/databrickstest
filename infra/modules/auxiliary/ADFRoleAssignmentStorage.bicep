// Copyright (c) Microsoft Corporation.
// Licensed under the MIT license.

// The module contains a template to create a role assignment of the ADF to a storage file system.
targetScope = 'resourceGroup'

// Parameters
param storageAccountFileSystemId string
param adfId string
param adfPrincipalId string
// Variables
var storageAccountFileSystemName = length(split(storageAccountFileSystemId, '/')) >= 13 ? last(split(storageAccountFileSystemId, '/')) : 'incorrectSegmentLength'
var storageAccountName = length(split(storageAccountFileSystemId, '/')) >= 13 ? split(storageAccountFileSystemId, '/')[8] : 'incorrectSegmentLength'
var adfSubscriptionId = length(split(adfId, '/')) >= 9 ? split(adfId, '/')[2] : subscription().subscriptionId
var adfResourceGroupName = length(split(adfId, '/')) >= 9 ? split(adfId, '/')[4] : resourceGroup().name
var adfName = length(split(adfId, '/')) >= 9 ? last(split(adfId, '/')) : 'incorrectSegmentLength'
//var roleDefinitionId = resourceId('Microsoft.Authorization/roleDefinitions', 'Storage Blob Data Contributor')
var roleDefinitionId = resourceId('Microsoft.Authorization/roleDefinitions', 'ba92f5b4-2d11-453d-a403-e96b0029c9fe')
// Resources
resource storageAccountFileSystem 'Microsoft.Storage/storageAccounts/blobServices/containers@2021-02-01' existing = {
  name: '${storageAccountName}/default/${storageAccountFileSystemName}'
}

// Resources
// resource storageAccount 'Microsoft.Storage/storageAccounts@2021-02-01' existing = {
//   name: '${storageAccountName}'
// }

// resource adf 'Microsoft.DataFactory/factories@2018-06-01' existing = {
//   name: adfName
//   scope: resourceGroup(adfSubscriptionId, adfResourceGroupName)
// }

// Assignment "Storage Blob Data Contributor" Role
// Get-AzRoleDefinition -Id 'ba92f5b4-2d11-453d-a403-e96b0029c9fe'
// var roleAssignmentName = guid(uniqueString(storageAccountFileSystem.id, adfId))
var roleAssignmentName = guid(storageAccountFileSystem.id, adfId)
resource adfRoleAssignment 'Microsoft.Authorization/roleAssignments@2020-04-01-preview' = {
  name: roleAssignmentName
  scope: storageAccountFileSystem
  properties: {
    roleDefinitionId: roleDefinitionId
    principalId: adfPrincipalId
  }
}

// Outputs

output roleAssignmentId string = adfRoleAssignment.id
output roleAssignmentName string = adfRoleAssignment.name
