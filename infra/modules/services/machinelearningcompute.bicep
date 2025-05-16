// // Creates compute resources in the specified machine learning workspace
// // Includes Compute Instance, Compute Cluster and attached Azure Kubernetes Service compute types
// @description('Prefix for resource names')
// param prefix string

// @description('Azure Machine Learning workspace to create the compute resources in')
// param machineLearning string

// @description('Azure region of the deployment')
// param location string

// @description('Tags to add to the resources')
// param tags object

// @description('Resource ID of the compute subnet')
// param computeSubnetId string

// param machineLearningComputeInstanceAdministrators array = [
//   // {
//   //   userPrincipalName: ''
//   //   objectId: ''
//   //   publicSshKey: ''
//   // }
// ]
// @description('Specifies the environment of the deployment.')
// param environment string

// /*resource userAssignedIdentity 'Microsoft.ManagedIdentity/userAssignedIdentities@2022-01-31-preview'  = {
//   name: '${prefix}-${environment}-managed-identity'
//   location: location
// }*/

// resource machineLearningCluster001 'Microsoft.MachineLearningServices/workspaces/computes@2022-06-01-preview' = {
//   name: '${machineLearning}/cpucluster001'
//   location: location
//   tags: tags
//   identity: {
//     type: 'SystemAssigned'
//  //   type: 'UserAssigned'
//  //   userAssignedIdentities: {
//  //       '${userAssignedIdentity.id}': {}
//  //   }
//   }
//   properties: {
//     computeType: 'AmlCompute'
//     //computeLocation:cation
//     description: 'Machine Learning cluster 001'
//     disableLocalAuth: true
//     properties: {
//       vmPriority: 'Dedicated'
//       vmSize: 'Standard_DS3_v2'
//       enableNodePublicIp: true
//       isolatedNetwork: false
//       osType: 'Linux'
//       remoteLoginPortPublicAccess: 'Disabled'
//       scaleSettings: {
//         minNodeCount: 0
//         maxNodeCount: 5
//         nodeIdleTimeBeforeScaleDown: 'PT120S'
//       }
//       subnet: {
//         id: computeSubnetId
//       }
//     }
//   }
// }

// resource machineLearningComputeInstance001 'Microsoft.MachineLearningServices/workspaces/computes@2022-05-01' = [for ci in machineLearningComputeInstanceAdministrators : if (!empty(ci.userPrincipalName)) {
//     // Name must be between 0 - 24
//   name: '${machineLearning}/${substring('${prefix}-${replace(substring(ci.userPrincipalName,0,indexOf(ci.userPrincipalName,'@')), '_', '')}',0,min(22,length('${prefix}-${replace(substring(ci.userPrincipalName,0,indexOf(ci.userPrincipalName,'@')), '_', '')}')))}CI'
//   location: location
//   tags: tags
//   identity: {
//     type: 'SystemAssigned'
//   }
//   properties: {
//     computeType: 'ComputeInstance'
//     computeLocation: location
//     description: 'Machine Learning compute instance 001'
//     disableLocalAuth: true
//     properties: {
//       applicationSharingPolicy: 'Personal'
//       computeInstanceAuthorizationType: 'personal'
//       personalComputeInstanceSettings: {
//         assignedUser: {
//           objectId: ci.objectId
//           tenantId: subscription().tenantId
//         }
//       }
//       sshSettings: {
//         sshPublicAccess: 'Disabled'
//       }
//       subnet: {
//         id: computeSubnetId
//       }
//       vmSize: 'Standard_DS3_v2'
//     }
//   }
// }]

// // Outputs

// output computeClusterPrincipalId string = machineLearningCluster001.identity.principalId
