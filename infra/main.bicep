// Copyright (c) Microsoft Corporation.
// Licensed under the MIT license.

targetScope = 'resourceGroup'

// General parameters
@description('Specifies the location for all resources.')
param location string
@allowed([
  'dev'
  'stg'
  'prd'
])
@description('Specifies the environment of the deployment.')
param environment string
@minLength(2)
@maxLength(10)
@description('Specifies the prefix for all resources created in this deployment.')
param prefix string
@description('Specifies the data product name.')
param dataProductName string
@description('Specifies the data product team ID.')
param dataProductTeamId string
@description('Specifies the tags that you want to apply to all resources.')
param tags object = {}
// param dbricksvnetId string
param virtualNetworkId string
@secure()
param clientsecret string

// Resource parameters
@description('Specifies the Azure subscription where the data product resources will be deployed.')
param subscriptionId string = ''
@description('Specifies the Azure subscription where the Syneos data lake is deployed.')
param syneos_data_lake_subscriptionId string = ''
@description('Specifies the Azure subscription where the data management resources are deployed.')
param data_management_subscriptionId string = ''
@allowed([
  'none'
  'sql'
  'mysql'
  'maria'
  'postgre'
])
@description('Specifies the sql flavour that will be deployed (None, SQL Server, MySQL Server, MariaDB Server, PostgreSQL Server).')
param sqlFlavour string = 'sql'
@secure()
@description('Specifies the administrator password of the sql servers in Synapse. If you selected dataFactory as processingService, leave this value empty as is.')
param administratorPassword string = ''

// @description('Specifies the list of data assets which will be implemeted as datasets in the Machine Learning workspace. If you do not want to connect any data assets, provide an empty list.')
// param amlDatasets array = [
//   {
//     name: ''
//     type: ''
//     datastoreName: ''
//     relativePath: ''    
//     sourceType: ''
//   }
// ]

@description('Specifies whether Azure Cosmos DB should be deployed as part of the template.')
param enableCosmos bool = false
@description('Specifies whether AzureML workspace should be deployed as part of the template.')
param enableAzureML bool = true
@description('Specifies whether Data Factory workspace should be deployed as part of the template.')
param enableDataFactory bool = true
@description('Specifies whether role assignments should be enabled.')
param enableRoleAssignments bool = true
// @description('Specifies whether databricks should be enabled.')
// param enableDatabricks bool = true

// Monitoring parameters
@description('Specifies whether monitoring capabilities should be enabled.')
param enableMonitoring bool = true
@description('Specifies the email ID of the alerts receiver.')
param dataProductTeamEmail string = ''

// Network parameters
@description('Specifies the resource ID of the subnet to which all services will connect.')
param subnetName string

// Repository parameters
param repoConfiguration object = {
  projectName: 'SyNeos Analytics Platform'
  repositoryName: 'Data Product Template'
  accountName: 'Syneos-IEP-IT-3595'
  collaborationBranch: 'main'
  rootFolder: '/code/adf/'
}
@description('Specifies the resourceGroup name that holds related resources for the solution.')
param resourceGroupName string = ''
// @description('Specifies the resource ID of the Databricks workspace that will be connected to the Machine Learning Workspace. If you do not want to connect Databricks to Machine Learning, leave this value empty as is.')
// param databricksWorkspaceId string = ''
// @description('Specifies the workspace URL of the Databricks workspace that will be connected to the Machine Learning Workspace. If you do not want to connect Databricks to Machine Learning, leave this value empty as is.')
// param databricksWorkspaceUrl string = ''
// @secure()
// @description('Specifies the access token of the Databricks workspace that will be connected to the Machine Learning Workspace. If you do not want to connect Databricks to Machine Learning, leave this value empty as is.')
// param databricksAccessToken string = ''

// param databricksvnetAddressPrefixId string = '10.233'

@description('Specifies the object IDs of the users who gets assigned to compute instances in the Machine Learning Workspace. If you do not want to create any Compute Instance, leave this value empty as is.')
param machineLearningComputeInstanceAdministrators array = [
  {
    userPrincipalName: ''
    objectId: ''
    publicSshKey: ''
  }
]
@description('Specifies the storage account name related with Purview.')
param purviewStorageAccount string = ''
@description('Specifies the event hub namespace related with Purview.')
param purviewEventHub string = ''
param enableOpenAi bool = false

// Variables
var name = prefix == 'coredlz' ? toLower('${dataProductName}-cr-${environment}') : toLower('${dataProductName}-${environment}')
var openAiName = '${name}-openai001'
var cognitiveSearchName = '${name}-searchservice001'
var formRecognizerName = '${name}-formrecognizer001'
var translatorName = '${name}-translator001'
var administratorUsername = 'SqlMainUser'

// Specifies the resource ID of the default storage account file system for Synapse
var synapseDefaultStorageAccountFileSystemId = '/subscriptions/${subscriptionId}/resourceGroups/${prefix}-${environment}-storage/providers/Microsoft.Storage/storageAccounts/${prefix}${environment}raw/blobServices/default/containers/demodp'
var synapseDefaultStorageAccountSubscriptionId = length(split(synapseDefaultStorageAccountFileSystemId, '/')) >= 13 ? split(synapseDefaultStorageAccountFileSystemId, '/')[2] : subscription().subscriptionId
var synapseDefaultStorageAccountResourceGroupName = length(split(synapseDefaultStorageAccountFileSystemId, '/')) >= 13 ? split(synapseDefaultStorageAccountFileSystemId, '/')[4] : resourceGroup().name
var keyVault001Name = '${name}-vault001'
//var synapse001Name = '${name}-synapse001'
var datafactory001Name = '${name}-datafactory001'
var cosmosdb001Name = '${name}-cosmos001'
var database001Name = 'Database001'
var sql001Name = '${name}-sqlserver001'
var mysql001Name = '${name}-mysql001'
var mariadb001Name = '${name}-mariadb001'
var potsgresql001Name = '${name}-postgresql001'

var applicationInsights001Name = '${name}-insights001'
//var containerRegistry001Name = '${name}-containerregistry001'
var storage001Name = '${name}-storage001'
//var machineLearning001Name = '${name}-machinelearning001'

// var databricks001Name = '${name}-databricks001'

var logAnalytics001Name = '${name}-loganalytics001'
var dataFactoryEmailActionGroup = '${datafactory001Name}-emailactiongroup'
var adfPipelineFailedAlertName = '${datafactory001Name}-failedalert'
//var synapsePipelineFailedAlertName = '${synapse001Name}-failedalert'
var cosmosRequestLimitedAlertName = '${cosmosdb001Name}-requestratealert'
var dashboardName = '${name}-dashboard'

// Purview variables
var purviewId  = '/subscriptions/${data_management_subscriptionId}/resourceGroups/iepdmlz-${environment}-governance/providers/Microsoft.Purview/accounts/iepdmlz-${environment}-purview001'
var purviewManagedStorageId = '/subscriptions/${data_management_subscriptionId}/resourceGroups/iepdmlz-${environment}-purview001/providers/Microsoft.Storage/storageAccounts/${purviewStorageAccount}'
var purviewManagedEventHubId = '/subscriptions/${data_management_subscriptionId}/resourceGroups/iepdmlz-${environment}-purview001/providers/Microsoft.EventHub/namespaces/${purviewEventHub}'

// Private DNS Zone variables
var privateDnsZoneIdKeyVault = '/subscriptions/${data_management_subscriptionId}/resourceGroups/iepdmlz-${environment}-global-dns/providers/Microsoft.Network/privateDnsZones/privatelink.vaultcore.azure.net'
var privateDnsZoneIdDataFactory = '/subscriptions/${data_management_subscriptionId}/resourceGroups/iepdmlz-${environment}-global-dns/providers/Microsoft.Network/privateDnsZones/privatelink.datafactory.azure.net'
var privateDnsZoneIdDataFactoryPortal = '/subscriptions/${data_management_subscriptionId}/resourceGroups/iepdmlz-${environment}-global-dns/providers/Microsoft.Network/privateDnsZones/privatelink.adf.azure.com'
var privateDnsZoneIdCosmosdbSql = 'subscriptions/${data_management_subscriptionId}/resourceGroups/iepdmlz-${environment}-global-dns/providers/Microsoft.Network/privateDnsZones/privatelink.documents.azure.com'
var privateDnsZoneIdSqlServer = '/subscriptions/${data_management_subscriptionId}/resourceGroups/iepdmlz-${environment}-global-dns/providers/Microsoft.Network/privateDnsZones/privatelink.database.windows.net'
var privateDnsZoneIdMySqlServer = '/subscriptions/${data_management_subscriptionId}/resourceGroups/iepdmlz-${environment}-global-dns/providers/Microsoft.Network/privateDnsZones/privatelink.mysql.database.azure.com'
var privateDnsZoneIdMariaDb = '/subscriptions/${data_management_subscriptionId}/resourceGroups/iepdmlz-${environment}-global-dns/providers/Microsoft.Network/privateDnsZones/privatelink.mariadb.database.azure.com'
var privateDnsZoneIdPostgreSql = '/subscriptions/${data_management_subscriptionId}/resourceGroups/iepdmlz-${environment}}-global-dns/providers/Microsoft.Network/privateDnsZones/privatelink.postgres.database.azure.com'
//var privateDnsZoneIdContainerRegistry = '/subscriptions/${data_management_subscriptionId}/resourceGroups/iepdmlz-${environment}-global-dns/providers/Microsoft.Network/privateDnsZones/privatelink.azurecr.io'
var privateDnsZoneIdBlob = '/subscriptions/${data_management_subscriptionId}/resourceGroups/iepdmlz-${environment}-global-dns/providers/Microsoft.Network/privateDnsZones/privatelink.blob.core.windows.net'
var privateDnsZoneIdFile = '/subscriptions/${data_management_subscriptionId}/resourceGroups/iepdmlz-${environment}-global-dns/providers/Microsoft.Network/privateDnsZones/privatelink.file.core.windows.net'
//var privateDnsZoneIdMachineLearningApi = '/subscriptions/${data_management_subscriptionId}/resourceGroups/iepdmlz-${environment}-global-dns/providers/Microsoft.Network/privateDnsZones/privatelink.api.azureml.ms'
//var privateDnsZoneIdMachineLearningNotebooks = '/subscriptions/${data_management_subscriptionId}/resourceGroups/iepdmlz-${environment}-global-dns/providers/Microsoft.Network/privateDnsZones/privatelink.notebooks.azure.net'

var rawDataLakeStorageId = '/subscriptions/${subscriptionId}/resourceGroups/${prefix}-${environment}-storage/providers/Microsoft.Storage/storageAccounts/${prefix}${environment}raw'
var workDataLakeStorageId = '/subscriptions/${subscriptionId}/resourceGroups/${prefix}-${environment}-storage/providers/Microsoft.Storage/storageAccounts/${prefix}${environment}work'
var encurDataLakeStorageId = '/subscriptions/${subscriptionId}/resourceGroups/${prefix}-${environment}-storage/providers/Microsoft.Storage/storageAccounts/${prefix}${environment}encur'
var storageResourceGroup = '${prefix}-${environment}-storage'

var subnetId = '/subscriptions/${subscriptionId}/resourceGroups/${prefix}-${environment}-network/providers/Microsoft.Network/virtualNetworks/${prefix}-${environment}-vnet/subnets/${subnetName}'
var iepTempVnetSubnetId = '/subscriptions/${subscriptionId}/resourceGroups/${prefix}-${environment}-network/providers/Microsoft.Network/virtualNetworks/iep-temp-vnet/subnets/default-subnet'

// Specifies the list of resource IDs of Data Lake Gen2 Containers which will be connected as datastores in the Machine Learning workspace. 
var datalakeFileSystems = [
    {'name': 'raw_zone', 'subscriptionId': subscriptionId, 'resourceGroup': '${prefix}-${environment}-storage', 'accountName':'${prefix}${environment}raw', 'filesystem': ''}
    {'name': 'enriched_and_curated_zone', 'subscriptionId': subscriptionId, 'resourceGroup': '${prefix}-${environment}-storage', 'accountName':'${prefix}${environment}encur', 'filesystem': ''}
    {'name': 'working_zone', 'subscriptionId': subscriptionId, 'resourceGroup': '${prefix}-${environment}-storage', 'accountName':'${prefix}${environment}work', 'filesystem': ''}
    {'name': 'syneos_data_lake', 'subscriptionId': syneos_data_lake_subscriptionId, 'resourceGroup': 'Z1DEUSENTDATALAKE_RG', 'accountName':'z1deusadlsstoracct01', 'filesystem': 'llap-z1deusdatalake' }
]



// Resources
module keyVault001 'modules/services/keyvault.bicep' = {
  name: 'keyVault001'
  scope: resourceGroup()
  params: {
    location: location
    tags: tags
    keyvaultName: keyVault001Name
    subnetId: subnetId
    privateDnsZoneIdKeyVault: privateDnsZoneIdKeyVault
    //enablePurgeProtection: environment == 'prd' ? true : false
  }
}

module datafactory001 'modules/services/datafactory.bicep' = if (enableDataFactory) {
  name: 'datafactory001'
  scope: resourceGroup()
  params: {
    location: location
    datafactoryName: datafactory001Name
    tags: tags
    subnetId: subnetId
    keyVault001Id: keyVault001.outputs.keyvaultId
    privateDnsZoneIdDataFactory: privateDnsZoneIdDataFactory
    privateDnsZoneIdDataFactoryPortal: privateDnsZoneIdDataFactoryPortal
    purviewId: purviewId
    purviewManagedStorageId: purviewManagedStorageId
    purviewManagedEventHubId: purviewManagedEventHubId
    rawDataLakeStorageId: rawDataLakeStorageId
    repoConfiguration: 'dev' == environment ? repoConfiguration : {}
  }
}

module cosmosdb001 'modules/services/cosmosdb.bicep' = if (enableCosmos) {
  name: 'cosmos001'
  scope: resourceGroup()
  params: {
    location: location
    tags: tags
    cosmosdbName: cosmosdb001Name
    subnetId: subnetId
    privateDnsZoneIdCosmosdbSql: privateDnsZoneIdCosmosdbSql
  }
}

module sql001 'modules/services/sql.bicep' = if (sqlFlavour == 'sql') {
  name: 'sql001'
  scope: resourceGroup()
  params: {
    location: location
    tags: tags
    sqlserverName: sql001Name
    subnetId: subnetId
    administratorUsername: administratorUsername
    administratorPassword: administratorPassword
    privateDnsZoneIdSqlServer: privateDnsZoneIdSqlServer
    database001Name: database001Name
    sqlserverAdminGroupName: ''
    sqlserverAdminGroupObjectID: ''
  }
}

module mysql001 'modules/services/mysql.bicep' = if (sqlFlavour == 'mysql') {
  name: 'mysql001'
  scope: resourceGroup()
  params: {
    location: location
    tags: tags
    mysqlserverName: mysql001Name
    subnetId: subnetId
    administratorUsername: administratorUsername
    administratorPassword: administratorPassword
    privateDnsZoneIdMySqlServer: privateDnsZoneIdMySqlServer
    mysqlserverAdminGroupName: ''
    mysqlserverAdminGroupObjectID: ''
  }
}

module mariadb001 'modules/services/mariadb.bicep' = if (sqlFlavour == 'maria') {
  name: 'mariadb001'
  scope: resourceGroup()
  params: {
    location: location
    mariadbName: mariadb001Name
    tags: tags
    subnetId: subnetId
    administratorUsername: administratorUsername
    administratorPassword: administratorPassword
    privateDnsZoneIdMariaDb: privateDnsZoneIdMariaDb
  }
}

module postgresql001 'modules/services/postgresql.bicep' = if (sqlFlavour == 'postgre') {
  name: 'postgresql001'
  scope: resourceGroup()
  params: {
    location: location
    postgresqlName: potsgresql001Name
    tags: tags
    subnetId: subnetId
    administratorUsername: administratorUsername
    administratorPassword: administratorPassword
    postgresqlAdminGroupName: ''
    postgresqlAdminGroupObjectID: ''
    privateDnsZoneIdPostgreSql: privateDnsZoneIdPostgreSql
  }
}
//AzureML
module applicationInsights001 'modules/services/applicationinsights.bicep' = if (enableAzureML) {
  name: 'applicationInsights001'
  scope: resourceGroup()
  params: {
    location: location
    tags: tags
    applicationInsightsName: applicationInsights001Name
    logAnalyticsWorkspaceId: ''
  }
}

// module containerRegistry001 'modules/services/containerregistry.bicep' = if (enableAzureML) {
//   name: 'containerRegistry001'
//   scope: resourceGroup()
//   params: {
//     location: location
//     tags: tags
//     containerRegistryName: containerRegistry001Name
//   }
// }

module storage001 'modules/services/storage.bicep' = if (enableAzureML) {
  name: 'storage001'
  scope: resourceGroup()
  params: {
    location: location
    tags: tags
    subnetId: subnetId
    storageName: storage001Name
    storageContainerNames: [
      'default'
    ]
    storageSkuName: 'Standard_LRS'
    privateDnsZoneIdBlob: privateDnsZoneIdBlob
    privateDnsZoneIdFile: privateDnsZoneIdFile
  }
}

// module machineLearning001 'modules/services/machinelearning.bicep' = if (enableAzureML) {
//   name: 'machineLearning001'
//   scope: resourceGroup()
//   params: {
//     prefix: dataProductName
//     location: location
//     tags: tags
//     machineLearningName: machineLearning001Name
//     applicationInsightsId: enableAzureML ? applicationInsights001.outputs.applicationInsightsId : ''
//     containerRegistryId: enableAzureML ? containerRegistry001.outputs.containerRegistryId : ''
//     keyVaultId: keyVault001.outputs.keyvaultId
//     storageAccountId: enableAzureML ? storage001.outputs.storageId : ''
//     computeSubnetId: iepTempVnetSubnetId
//     datalakeFileSystems: datalakeFileSystems
//     resourceGroupName: resourceGroupName
//     datasets: amlDatasets
//     machineLearningComputeInstanceAdministrators: machineLearningComputeInstanceAdministrators
//     env: environment
//   }
// }

// AzureML
module logAnalytics001 'modules/services/loganalytics.bicep' = if (enableMonitoring) {
  name: 'logAnalytics001'
  scope: resourceGroup()
  params: {
    location: location
    tags: tags
    logAnalyticsName: logAnalytics001Name
    //? processingService: processingService
    sqlFlavour: sqlFlavour
    enableDataFactory: enableDataFactory
  }
}

module diagnosticSettings './modules/services/diagnosticsettings.bicep' = if (enableMonitoring) {
  name: 'diagnosticSettings'
  scope: resourceGroup()
  params: {
    datafactoryName: enableDataFactory ? datafactory001.outputs.dataFactoryName : ''
    logAnalytics001Name: enableMonitoring ? logAnalytics001.outputs.logAnalyticsWorkspaceName : ''
    //? processingService: processingService
    enableDataFactory: enableDataFactory
    sqlFlavour: sqlFlavour
    mysql001Name: sqlFlavour == 'mysql' ? mysql001.outputs.mysqlName : ''
    sqlServerName: sqlFlavour == 'sql' ? sql001.outputs.sqlserverName : ''
    mariadb001Name: sqlFlavour == 'maria' ? mariadb001.outputs.mariadbName : ''
    potsgresql001Name: sqlFlavour == 'postgre' ? postgresql001.outputs.postgresqlName : ''
    enableCosmos: enableCosmos
    cosmosdb001Name: enableCosmos ? cosmosdb001.outputs.cosmosName : ''
    enableOpenAi: enableOpenAi
    openAiName: openAiName
    // databricksName: databricksServices.outputs.databricksName
    sqlServerDatabases: [
      sqlFlavour == 'sql' ? sql001.outputs.sqlserverDatabase001Name : null
    ]
  }
}

module alerts './modules/services/alerts.bicep' = if (!empty(dataProductTeamEmail) && enableMonitoring) {
  name: 'alerts'
  scope: resourceGroup()
  params: {
    adfPipelineFailedAlertName: adfPipelineFailedAlertName
    datafactoryScope: enableDataFactory ? datafactory001.outputs.dataFactoryId : ''
    dataFactoryEmailActionGroup: dataFactoryEmailActionGroup
    dataProductTeamEmail: dataProductTeamEmail
    location: location
    //?processingService: processingService
    enableDataFactory: enableDataFactory
    cosmosRequestLimitedAlertName: cosmosRequestLimitedAlertName
    enableCosmos: enableCosmos
    cosmosDBScope: enableCosmos ? cosmosdb001.outputs.cosmosId : ''
    tags: tags
  }
}

module dashboards './modules/services/dashboard.bicep' = if (enableMonitoring) {
  name: 'dashboard'
  scope: resourceGroup()
  params: {
    dashboardName: dashboardName
    datafactoryName: enableDataFactory ? datafactory001.outputs.dataFactoryName : ''
    datafactoryScope: enableDataFactory ? datafactory001.outputs.dataFactoryId : ''
    openAiAcope: enableOpenAi ? openAiServices.outputs.openAiId : ''
    location: location
    //? processingService: processingService
    enableDataFactory: enableDataFactory
    enableOpenAi: enableOpenAi
    tags: tags
  }
}


// Creates Databricks workspace
// module databricksServices 'modules/services/databricks.bicep' = if (enableDatabricks) {
//   name: 'databricksServices'
//   scope: resourceGroup()
//   params: {
//     environment: environment
//     name: name
//     location: location
//     databricksName: databricks001Name
//     dbricksvnetId: dbricksvnetId
//     dbricksPubSubnet: '${dataProductName}PublicSubnet'
//     dbricksPrivSubnet: '${dataProductName}PrivateSubnet'
//     vnetAddressPrefixId: databricksvnetAddressPrefixId
//     rg: string(resourceGroup())
//     tags: {
//       Environment: 'DEV'
//       Toolkit: 'Bicep'
//       LOB: 'IEP'
//       CreatedBy: 'SNAP-Team@syneoshealth.com'
//       PMOID: 'IT_3595'
//       LifeCycleState: 'Active'
//       CreatedOn: ''
//       CostCenter: 'IEP_4595'
//       Application: 'SNAP-Platform'
//       ApplicationOwner: 'ries.guthmann@syneoshealth.com'
//       BusinessOwner: 'darren.coleman@syneoshealth.com'
//       ServiceNowRequest: ''
//       Alignment: 'IEP (SNAP)'
//     }
//   }
// }

// cost dashboard
module costDashboard './modules/services/costdashboard.bicep' = {
  name: 'costdashboard'
  scope: resourceGroup()
  params: {
    dashboardName: dataProductName 
    location: location
    tags: tags
    resourceGroupName: resourceGroupName
    subscriptionId: subscriptionId
    environment: environment
  }
}

// Azure OpenAI
module openAiServices 'modules/services/openai.bicep' = if (enableOpenAi == true) {
  name: 'openAiServices'
  scope: resourceGroup()
  params: {
    openAiName: openAiName
    location: location
    name: name
    tags: tags
    subnetId: subnetId
    virtualNetworkId: virtualNetworkId
    deployments: [
      {
        name: 'gpt-35-turbo-16k'
        sku: {
          name: 'Standard'
          capacity: '60'
        }
        model: {
          format: 'OpenAI'
          name: 'gpt-35-turbo-16k'
          version: '0613'
        }
      }
      {
        name: 'text-davinci-003'
        sku: {
          name: 'Standard'
          capacity: '20'
        }
        model: {
          format: 'OpenAI'
          name: 'text-davinci-003'
          version: '1'
        }
      }
      {
        name: 'text-embedding-ada-002'
        sku: {
          name: 'Standard'
          capacity: '30'
        }
        model: {
          format: 'OpenAI'
          name: 'text-embedding-ada-002'
          version: '2'
        }
      }
    ]
    cognitiveSearchName: cognitiveSearchName
    formRecognizerName: formRecognizerName
    translatorName: translatorName
  }
}

// Role Assignments
module roleAssignmentDefaultRawContainer 'modules/auxiliary/containerRoleAssignment.bicep' = if (enableRoleAssignments) {
  name: 'roleAssignmentRawContainer'
  scope: resourceGroup(subscriptionId, storageResourceGroup)
  params: {
    storageAccountFileSystemId: '${rawDataLakeStorageId}/blobServices/default/containers/${dataProductName}'
    roleAssignments: [
      {
        principalId: enableDataFactory ? datafactory001.outputs.dataFactoryPrincipalId : ''
        role: 'Storage Blob Data Contributor'
      }
    ]
  }
  dependsOn: [ datafactory001 ]
}

module roleAssignmentDefaultWorkContainer 'modules/auxiliary/containerRoleAssignment.bicep' = if (enableRoleAssignments) {
  name: 'roleAssignmentWorkContainer'
  scope: resourceGroup(subscriptionId, storageResourceGroup)
  params: {
    storageAccountFileSystemId: '${workDataLakeStorageId}/blobServices/default/containers/${dataProductName}'
    roleAssignments: [
      {
        principalId: enableDataFactory ? datafactory001.outputs.dataFactoryPrincipalId : ''
        role: 'Storage Blob Data Contributor'
      }
    ]
  }
  dependsOn: [ datafactory001 ]
}

module roleAssignmentDefaultWEncurContainer 'modules/auxiliary/containerRoleAssignment.bicep' = if (enableRoleAssignments) {
  name: 'roleAssignmentEncurContainer'
  scope: resourceGroup(subscriptionId, storageResourceGroup)
  params: {
    storageAccountFileSystemId: '${encurDataLakeStorageId}/blobServices/default/containers/${dataProductName}'
    roleAssignments: [
      {
        principalId: enableDataFactory ? datafactory001.outputs.dataFactoryPrincipalId : ''
        role: 'Storage Blob Data Contributor'
      }
    ]
  }
  dependsOn: [ datafactory001 ]
}

module roleAssignmentSynapseDefaultStorage 'modules/auxiliary/containerRoleAssignment.bicep' = if (enableRoleAssignments) {
  name: 'roleAssignmentSynapseStorage'
  scope: resourceGroup(synapseDefaultStorageAccountSubscriptionId, synapseDefaultStorageAccountResourceGroupName)
  params: {
    storageAccountFileSystemId: synapseDefaultStorageAccountFileSystemId
    roleAssignments: [
      {
        principalId: enableDataFactory ? datafactory001.outputs.dataFactoryPrincipalId : ''
        role: 'Storage Blob Data Contributor'
      }
    ]
  }
  dependsOn: [ datafactory001 ]
}

module roleAssignmentRaw 'modules/auxiliary/storageRoleAssignment.bicep' = if (enableRoleAssignments) {
  name: 'roleAssignmentRaw'
  scope: resourceGroup(subscriptionId, storageResourceGroup)
  params: {
    storageAccountFileSystemId: rawDataLakeStorageId
    roleAssignments: [
      {
        principalId: enableDataFactory ? datafactory001.outputs.dataFactoryPrincipalId : ''
        role: 'Storage Blob Data Reader'
      }
    ]
  }
  dependsOn: [ datafactory001 ]
}

module roleAssignmentWork 'modules/auxiliary/storageRoleAssignment.bicep' = if (enableRoleAssignments) {
  name: 'roleAssignmentWork'
  scope: resourceGroup(subscriptionId, storageResourceGroup)
  params: {
    storageAccountFileSystemId: workDataLakeStorageId
    roleAssignments: [
      {
        principalId: enableDataFactory ? datafactory001.outputs.dataFactoryPrincipalId : ''
        role: 'Storage Blob Data Reader'
      }
    ]
  }
  dependsOn: [ datafactory001 ]
}

module roleAssignmentEncur 'modules/auxiliary/storageRoleAssignment.bicep' = if (enableRoleAssignments) {
  name: 'roleAssignmentEncur'
  scope: resourceGroup(subscriptionId, storageResourceGroup)
  params: {
    storageAccountFileSystemId: encurDataLakeStorageId
    roleAssignments: [
      {
        principalId: enableDataFactory ? datafactory001.outputs.dataFactoryPrincipalId : ''
        role: 'Storage Blob Data Reader'
      }
    ]
  }
  dependsOn: [ datafactory001 ]
}

// module roleAssignmentMachineLearning 'modules/auxiliary/amlRoleAssignment.bicep' = if (enableAzureML && enableRoleAssignments) {
//   name: '${machineLearning001Name}-RoleAssignment'
//   scope: resourceGroup()
//   params: {
//     machineLearningName: machineLearning001Name
//     roleAssignments: [
//       {
//         principalId: enableDataFactory ? datafactory001.outputs.dataFactoryPrincipalId : ''
//         role: 'Contributor'
//       }
//       {
//         principalId: enableAzureML ? machineLearning001.outputs.computeClusterPrincipalId : ''
//         role: 'Contributor'
//       }
//       {
//         principalId: environment == 'dev' ? dataProductTeamId : ''
//         role: 'AzureML Data Scientist'
//       }
//     ]
//   }
//   dependsOn:  [ datafactory001, machineLearning001 ]
// }

module roleAssignmentDataFactory 'modules/auxiliary/adfRoleAssignment.bicep' = if (enableDataFactory && enableRoleAssignments) {
  name: '${datafactory001Name}-RoleAssignment'
  scope: resourceGroup()
  params: {
    datafactoryName: datafactory001Name
    roleAssignments: [
      {
        principalId: environment == 'dev' ? dataProductTeamId : ''
        role: 'Data Factory Contributor'
      }
    ]
  }
  dependsOn:  [ datafactory001 ]
}

module roleAssignmentKeyVault 'modules/auxiliary/keyVaultRoleAssignment.bicep' = if (enableDataFactory && enableRoleAssignments) {
  name: '${keyVault001Name}-RoleAssignment'
  scope: resourceGroup()
  params: {
    keyVaultName: keyVault001Name
    roleAssignments: [
      {
        principalId: enableDataFactory ? datafactory001.outputs.dataFactoryPrincipalId : ''
        role: 'Key Vault Secrets User'
      }
    ]
  }
  dependsOn: [
    datafactory001
    keyVault001
  ]
}

// module roleAssignmentDatabricks 'modules/auxiliary/databricksRoleAssignment.bicep' = if (enableRoleAssignments) {
//   name: '${databricks001Name}-RoleAssignment'
//   scope: resourceGroup()
//   params: {
//     databricksName: databricks001Name
//     roleAssignments: [
//       {
//         principalId: enableDataFactory ? datafactory001.outputs.dataFactoryPrincipalId : ''
//         role: 'Contributor'
//       }
//     ]
//   }
//   dependsOn:  [
//     datafactory001
//     databricksServices
//   ]
// }

// // Outputs
// output databricksServiceApiUrl string = enableDatabricks ? databricksServices.outputs.databricksApiUrl : ''
// output databricksServiceId string = enableDatabricks ? databricksServices.outputs.databricksId : ''
// output databricksServiceSubscriptionId string = enableDatabricks ? split(databricksServices.outputs.databricksId, '/')[2] : ''
// output databricksServiceResourceGroupName string = enableDatabricks ? split(databricksServices.outputs.databricksId, '/')[4] : ''
// output databricksServiceName string = enableDatabricks ? any(last(split(databricksServices.outputs.databricksId, '/'))) : ''
