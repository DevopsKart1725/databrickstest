// This template is used to create a Azure Open AI, Serach Service, Formrecognizer and Translator
targetScope = 'resourceGroup'

// Parameters
param location string
param tags object
param name string
param openAiName string
param openAiSkuName object = {
  name: 'S0'
}
param deployments array
param virtualNetworkId string
param subnetId string
param cognitiveSearchName string
@description('The SKU of the search service you want to create. E.g. free or standard')
@allowed([
  'free'
  'basic'
  'standard'
  'standard2'
  'standard3'
])
param cognitiveSearchSku string = 'standard'
// param openAiPrivateIPAddress string
// param AzureCognitiveSearchPrivateIPAddress string
param formRecognizerName string
param translatorName string

resource account 'Microsoft.CognitiveServices/accounts@2023-05-01' = {
  name: openAiName
  location: location
  tags: tags
  kind: 'OpenAI'
  properties: {
    customSubDomainName: openAiName
    publicNetworkAccess: 'Disabled'
    networkAcls: {
      defaultAction: 'Allow'
    }
  }
  sku: openAiSkuName
}

@batchSize(1)
resource deployment 'Microsoft.CognitiveServices/accounts/deployments@2023-05-01' = [for deployment in deployments: {
  parent: account
  name: deployment.name
  sku: deployment.sku
  properties: {
    model: deployment.model
    raiPolicyName: contains(deployment, 'raiPolicyName') ? deployment.raiPolicyName : null
  }
}]

resource openAiPrivateEndpoint 'Microsoft.Network/privateEndpoints@2020-11-01' = {
  name: '${name}-openai-privateendpoint'
  location: location
  tags: tags
  properties: {
    manualPrivateLinkServiceConnections: []
    privateLinkServiceConnections: [
      {
        name: '${name}-openai-privateendpoint'
        properties: {
          groupIds: [
            'account'
          ]
          privateLinkServiceId: account.id
          requestMessage: ''
        }
      }
    ]
    subnet: {
      id: subnetId
    }
  }
}

resource openAiPrivateDnsZone 'Microsoft.Network/privateDnsZones@2020-06-01' = {
  name: 'privatelink.openai01.azure.com'
  location: 'global'
  tags: tags
}

resource openAiPrivateDnsZoneLink 'Microsoft.Network/privateDnsZones/virtualNetworkLinks@2020-06-01' = {
  parent: openAiPrivateDnsZone
  name: '${openAiPrivateDnsZone.name}-link'
  location: 'global'
  properties: {
    registrationEnabled: false
    virtualNetwork: {
      id: virtualNetworkId
    }
  }
}

resource openAiPrivateDnsZoneGroup 'Microsoft.Network/privateEndpoints/privateDnsZoneGroups@2021-05-01' = {
  parent: openAiPrivateEndpoint
  name: 'default'
  location: location
  properties: {
    privateDnsZoneConfigs: [
      {
        name: 'privatelink-openai-azure-com'
        properties: {
          privateDnsZoneId: openAiPrivateDnsZone.id
        }
      }
    ]
  }
}

resource cognitiveSearch 'Microsoft.Search/searchServices@2020-08-01' = {
  name: cognitiveSearchName
  location: location
  sku: {
    name: cognitiveSearchSku
  }
  properties: {
    publicNetworkAccess: 'disabled'
    replicaCount: 1
    partitionCount: 1
  }
}

resource cognitiveSearchPrivateEndpoint 'Microsoft.Network/privateEndpoints@2020-11-01' = {
  name: '${name}-searchservice-privateendpoint'
  location: location
  tags: tags
  properties: {
    manualPrivateLinkServiceConnections: []
    privateLinkServiceConnections: [
      {
        name: '${name}-searchservice-privateendpoint'
        properties: {
          groupIds: [
            'searchService'
          ]
          privateLinkServiceId: cognitiveSearch.id
          requestMessage: ''
        }
      }
    ]
    subnet: {
      id: subnetId
    }
  }
}

resource cognitivesearchPrivateDnsZone 'Microsoft.Network/privateDnsZones@2020-06-01' = {
  name: 'privatelink.openaisearch.windows.net'
  location: 'global'
  tags: tags
}

resource cognitivesearchPrivateDnsZoneLink 'Microsoft.Network/privateDnsZones/virtualNetworkLinks@2020-06-01' = {
  parent: cognitivesearchPrivateDnsZone
  name: '${cognitivesearchPrivateDnsZone.name}-link'
  location: 'global'
  properties: {
    registrationEnabled: false
    virtualNetwork: {
      id: virtualNetworkId
    }
  }
}

resource cognitivesearchPrivateDnsZoneGroup 'Microsoft.Network/privateEndpoints/privateDnsZoneGroups@2021-05-01' = {
  parent: cognitiveSearchPrivateEndpoint
  name: 'default'
  location: location
  properties: {
    privateDnsZoneConfigs: [
      {
        name: 'privatelink-search-windows-net'
        properties: {
          privateDnsZoneId: cognitivesearchPrivateDnsZone.id
        }
      }
    ]
  }
}

resource formRecognizer 'Microsoft.CognitiveServices/accounts@2023-05-01' = {
  name: formRecognizerName
  location: location
  tags: tags
  sku: {
    name: 'S0'
  }
  kind: 'FormRecognizer'
  identity: {
    type: 'None'
  }
  properties: {
    networkAcls: {
      defaultAction: 'Allow'
      virtualNetworkRules: []
      ipRules: []
    }
    publicNetworkAccess: 'Enabled'
  }
}

resource translator 'Microsoft.CognitiveServices/accounts@2023-05-01' = {
  name: translatorName
  location: location
  tags: tags
  sku: {
    name: 'S1'
  }
  kind: 'TextTranslation'
  identity: {
    type: 'None'
  }
  properties: {
    networkAcls: {
      defaultAction: 'Allow'
      virtualNetworkRules: []
      ipRules: []
    }
    publicNetworkAccess: 'Enabled'
  }
}

output openAiId string = account.id
output openAiEndpoint string = 'https://${openAiName}.openai.azure.com/'
output searchServiceId string = cognitiveSearch.id
output formRecognizerId string = formRecognizer.id
output translatorId string = translator.id
output openAiName string = account.name
