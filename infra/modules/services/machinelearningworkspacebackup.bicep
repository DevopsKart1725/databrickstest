// // Creates a machine learning workspace code backup on storage fileshares

// @description('Specifies the data product name.')
// param dataProductName string
// @description('Specifies the storage account name.')
// param storageAccountName string = '${dataProductName}devstorage001'
// @description('Specifies the resourceGroup name that holds related resources for the solution.')
// param resourceGroupName string
// param fileShareName string = 'code-391ff5ac-6576-460f-ba4d-7e03433c68b6'
// param vaultName string = 'iep-dev-vault001'
// @description('Number of days for which the daily backup is to be retained.')
// param dailyRetentionDurationCount int = 30
// @description('Time of day when backup should be triggered in 24 hour HH:MM format, where MM must be 00 or 30.')
// param scheduleRunTime string = '05:00'
// @description('Any valid timezone, for example: UTC, Pacific Standard Time.')
// param timeZone string = 'UTC'

// var scheduleRunTimes = [
//   '2023-03-23T${scheduleRunTime}:00Z'
// ]

// // param baseTime string = utcNow('u')

// resource fileShareBackupPolicy 'Microsoft.RecoveryServices/vaults/backupPolicies@2021-12-01' = {
//   name: '${vaultName}/AMLWorkspaceBackup'
//   properties: {
//     backupManagementType: 'AzureStorage'
//     schedulePolicy: {
//       scheduleRunFrequency: 'Daily'
//       scheduleRunTimes: scheduleRunTimes
//       schedulePolicyType: 'SimpleSchedulePolicy'
//     }
//     retentionPolicy: {
//       dailySchedule: {
//         retentionTimes: scheduleRunTimes
//         retentionDuration: {
//           count: dailyRetentionDurationCount
//           durationType: 'Days'
//         }
//       }
//       retentionPolicyType: 'LongTermRetentionPolicy'
//     }
//     timeZone: timeZone
//     workLoadType: 'AzureFileShare'
//   }
// }

// resource protectionContainer 'Microsoft.RecoveryServices/vaults/backupFabrics/protectionContainers@2021-12-01' = {
//   name: '${vaultName}/Azure/storagecontainer;Storage;${resourceGroupName};${storageAccountName}'
//   properties: {
//     backupManagementType: 'AzureStorage'
//     containerType: 'StorageContainer'
//     sourceResourceId: resourceId(resourceGroupName, 'Microsoft.Storage/storageAccounts', storageAccountName)
//   }
//   dependsOn: [
//     fileShareBackupPolicy
//   ]
// }

// resource protectedItem 'Microsoft.RecoveryServices/vaults/backupFabrics/protectionContainers/protectedItems@2023-01-01' = {
//   parent: protectionContainer
//   name: 'AzureFileShare;${fileShareName}'
//   properties: {
//     protectedItemType: 'AzureFileShareProtectedItem'
//     sourceResourceId: resourceId(resourceGroupName, 'Microsoft.Storage/storageAccounts', storageAccountName)
//     policyId: fileShareBackupPolicy.id
//   }
// }
