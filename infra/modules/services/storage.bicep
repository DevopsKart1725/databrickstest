// Copyright (c) Microsoft Corporation.
// Licensed under the MIT license.

// This template is used to create a Storage account.
targetScope = 'resourceGroup'

// Parameters
param location string
param tags object
param subnetId string
param storageName string
@allowed([
  'Standard_LRS'
  'Standard_ZRS'
  'Standard_GRS'
  'Standard_GZRS'
  'Standard_RAGRS'
  'Standard_RAGZRS'
  'Premium_LRS'
  'Premium_ZRS'
])
param storageSkuName string = 'Standard_LRS'
param storageContainerNames array = [
  'default'
]
param privateDnsZoneIdBlob string = ''
param privateDnsZoneIdFile string = ''

// Variables
var storageNameCleaned = replace(storageName, '-', '')
var storagePrivateEndpointNameBlob = '${storage.name}-blob-private-endpoint'
var storagePrivateEndpointNameFile = '${storage.name}-file-private-endpoint'

// Resources

resource storage 'Microsoft.Storage/storageAccounts@2021-09-01' = {
  name: storageNameCleaned
  location: location
  tags: tags
  sku: {
    name: storageSkuName
  }
  kind: 'StorageV2'
  properties: {
    accessTier: 'Hot'
    allowBlobPublicAccess: false
    allowCrossTenantReplication: false
    allowSharedKeyAccess: true
    encryption: {
      keySource: 'Microsoft.Storage'
      requireInfrastructureEncryption: false
      services: {
        blob: {
          enabled: true
          keyType: 'Account'
        }
        file: {
          enabled: true
          keyType: 'Account'
        }
        queue: {
          enabled: true
          keyType: 'Service'
        }
        table: {
          enabled: true
          keyType: 'Service'
        }
      }
    }
    isHnsEnabled: false
    isNfsV3Enabled: false
    keyPolicy: {
      keyExpirationPeriodInDays: 7
    }
    largeFileSharesState: 'Disabled'
    minimumTlsVersion: 'TLS1_2'
    networkAcls: {
      bypass: 'AzureServices'
      defaultAction: 'Allow'
    }
    supportsHttpsTrafficOnly: true
  }
}

// storagePrivateEndpointBlob
resource storagePrivateEndpointBlob 'Microsoft.Network/privateEndpoints@2020-11-01' = {
  name: storagePrivateEndpointNameBlob
  location: location
  tags: tags
  properties: {
    manualPrivateLinkServiceConnections: []
    privateLinkServiceConnections: [
      {
        name: storagePrivateEndpointNameBlob
        properties: {
          groupIds: [
            'blob'
          ]
          privateLinkServiceId: storage.id
          requestMessage: ''
        }
      }
    ]
    subnet: {
      id: subnetId
    }
  }
}

resource storagePrivateEndpointBlobARecord 'Microsoft.Network/privateEndpoints/privateDnsZoneGroups@2020-11-01' = if (!empty(privateDnsZoneIdBlob)) {
  parent: storagePrivateEndpointBlob
  name: 'default'
  properties: {
    privateDnsZoneConfigs: [
      {
        name: '${storagePrivateEndpointBlob.name}-arecord'
        properties: {
          privateDnsZoneId: privateDnsZoneIdBlob
        }
      }
    ]
  }
}

// storagePrivateEndpointFile
resource storagePrivateEndpointFile 'Microsoft.Network/privateEndpoints@2020-11-01' = {
  name: storagePrivateEndpointNameFile
  location: location
  tags: tags
  properties: {
    manualPrivateLinkServiceConnections: []
    privateLinkServiceConnections: [
      {
        name: storagePrivateEndpointNameFile
        properties: {
          groupIds: [
            'file'
          ]
          privateLinkServiceId: storage.id
          requestMessage: ''
        }
      }
    ]
    subnet: {
      id: subnetId
    }
  }
}

resource storagePrivateEndpointFileARecord 'Microsoft.Network/privateEndpoints/privateDnsZoneGroups@2020-11-01' = if (!empty(privateDnsZoneIdBlob)) {
  parent: storagePrivateEndpointFile
  name: 'default'
  properties: {
    privateDnsZoneConfigs: [
      {
        name: '${storagePrivateEndpointFile.name}-arecord'
        properties: {
          privateDnsZoneId: privateDnsZoneIdFile
        }
      }
    ]
  }
}

// Outputs
output storageId string = storage.id
