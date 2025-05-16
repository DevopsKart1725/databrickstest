// Copyright (c) Microsoft Corporation.
// Licensed under the MIT license.

// This template is used to create a Databricks workspace.
targetScope = 'resourceGroup'

// Parameters
param environment string
param name string
param location string
param tags object
param databricksName string
param rg string
param dbricksvnetId string
param dbricksPubSubnet string
param dbricksPrivSubnet string
@description('Specifies the environment of the deployment.')
param vnetAddressPrefixId string

// Variables

// Resources
resource databricks 'Microsoft.Databricks/workspaces@2021-04-01-preview' =  {
  name: databricksName
  location: location
  tags: tags
  sku: {
    name: 'premium'
  }
  properties: {
    managedResourceGroupId: '${subscription().id}/resourceGroups/${databricksName}-rg'
    parameters: {
      customVirtualNetworkId: {
        value: dbricksvnetId
      }
      customPrivateSubnetName: {
        value: dbricksPrivSubnet
      }
      customPublicSubnetName: {
        value: dbricksPubSubnet
      }
      enableNoPublicIp: {
        value: true
      }
      prepareEncryption: {
        value: true
      }
      requireInfrastructureEncryption: {
        value: false
      }
      vnetAddressPrefix: {
        value: vnetAddressPrefixId
      }
    }
  }
}

// Outputs
output databricksId string = databricks.id
output databricksWorkspaceUrl string = databricks.properties.workspaceUrl
output databricksApiUrl string = 'https://${location}.azuredatabricks.net'
output databricksName string = databricks.name