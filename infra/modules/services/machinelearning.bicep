// // Creates a machine learning workspace, private endpoints and compute resources
// // Compute resources include a GPU cluster, CPU cluster, compute instance and attached private AKS cluster
// @description('Prefix for resource names')
// param prefix string

// @description('Azure region of the deployment')
// param location string

// @description('Tags to add to the resources')
// param tags object

// @description('Machine learning workspace name')
// param machineLearningName string

// @description('Resource ID of the application insights resource')
// param applicationInsightsId string

// @description('Resource ID of the container registry resource')
// param containerRegistryId string

// @description('Resource ID of the key vault resource')
// param keyVaultId string

// @description('Resource ID of the storage account resource')
// param storageAccountId string

// @description('Resource ID of the compute subnet')
// param computeSubnetId string

// @description('Specifies the resourceGroup name that holds related resources for the solution.')
// param resourceGroupName string
// param otherResourceGroup string = 'iepdlz01-dev-mgmt'

// param datalakeFileSystems array = [
//   {
//     name: ''
//     subscriptionId: ''
//     resourceGroup: ''
//     accountName: ''
//     filesystem: ''
//   }
// ]
// param datasets array = [
//   /*  {
//       name: ''
//       type: ''
//       datastoreName: ''
//       relativePath: ''
//       sourceType: ''
//     }*/
//   ]
// param machineLearningComputeInstanceAdministrators array = [
//   // {
//   //   userPrincipalName: ''
//   //   objectId: ''
//   //   publicSshKey: ''
//   // }
// ]

// @description('Specifies the environment of the deployment.')
// param env string

// // Variables
// var containerName = toLower(prefix)

// resource machineLearning 'Microsoft.MachineLearningServices/workspaces@2022-05-01' = {
//   name: machineLearningName
//   location: location
//   tags: tags
//   identity: {
//     type: 'SystemAssigned'
//   }
//   properties: {
//     // workspace organization
//     // dependent resources
//     applicationInsights: applicationInsightsId
//     containerRegistry: containerRegistryId
//     keyVault: keyVaultId
//     storageAccount: storageAccountId

//     // configuration for workspaces with private link endpoint
//     // imageBuildCompute: 'cluster001'
//     publicNetworkAccess: 'Enabled'
//   }
// }

// module machineLearningCompute 'machinelearningcompute.bicep' = {
//   name: 'machineLearningComputes'
//   scope: resourceGroup()
//   params: {
//     machineLearning: machineLearningName
//     location: location
//     computeSubnetId: computeSubnetId
//     prefix: prefix
//     tags: tags
//     machineLearningComputeInstanceAdministrators: machineLearningComputeInstanceAdministrators
//     environment: env
//   }
//   dependsOn: [
//     machineLearning
//   ]
// }

// resource machineLearningDatastores 'Microsoft.MachineLearningServices/workspaces/datastores@2022-06-01-preview' = [for (datalakeFileSystem, i) in datalakeFileSystems: if (!empty(datalakeFileSystem.name)) {
//   parent: machineLearning
//   name: datalakeFileSystem.name
//   properties: {
//     tags: tags
//     datastoreType: 'AzureDataLakeGen2'
//     accountName: datalakeFileSystem.accountName
//     endpoint: environment().suffixes.storage
//     filesystem: !empty(datalakeFileSystem.filesystem) ? datalakeFileSystem.filesystem : containerName
//     protocol: 'https'
//     resourceGroup: datalakeFileSystem.resourceGroup
//     serviceDataAccessAuthIdentity: 'None'
//     subscriptionId: datalakeFileSystem.subscriptionId
//     credentials: {
//       credentialsType: 'None'
//     }
//     description: 'Data Lake Gen2 - ${datalakeFileSystem.name}'
//   }
// }]

// module machineLearningWorkspaceBackup 'machinelearningworkspacebackup.bicep' = if (env == 'dev'){
//   name: 'machineLearningWorkspaceBackup'
//   scope: resourceGroup(otherResourceGroup)
//   params: {
//     dataProductName: toLower(prefix)
//     resourceGroupName: resourceGroupName
//   }
//   dependsOn: [
//     machineLearningDatastores
//   ]
// }

// resource machineLearningDatasets 'Microsoft.MachineLearningServices/workspaces/datasets@2020-05-01-preview' = [for (dataset, i) in datasets: if (!empty(dataset.name)) {
//   name:  '${dataset.name}'
//   parent: machineLearning
//   properties: {
//     datasetType: dataset.type
//     parameters: {
//       header: 'all_files_have_same_headers'
//       includePath: true
//       path: {
//         dataPath: {
//           datastoreName: dataset.datastoreName
//           relativePath: dataset.relativePath
//         }
//      }
//      sourceType: dataset.sourceType
//     }
//     registration: {
//       name: dataset.name
//     }
//     skipValidation: false
//   }
//   dependsOn: [
//     machineLearningDatastores
//   ]
// }]

// // Outputs
// output machineLearningId string = machineLearning.id
// output machineLearningPrincipalId string = machineLearning.identity.principalId
// output computeClusterPrincipalId string = machineLearningCompute.outputs.computeClusterPrincipalId
