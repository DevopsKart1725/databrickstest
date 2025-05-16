// Copyright (c) Microsoft Corporation.
// Licensed under the MIT license.

// This template is used to setup diagnostic settings.
targetScope = 'resourceGroup'

// Parameters
param logAnalytics001Name string
param datafactoryName string
//?param processingService string
param sqlServerDatabases array
param sqlServerName string
param mysql001Name string
param mariadb001Name string
param potsgresql001Name string
param cosmosdb001Name string
param sqlFlavour string
param enableCosmos bool
param enableDataFactory bool
param enableOpenAi bool
param openAiName string
// param  databricksName string
//variables
var sqlServerDatabasesCount = length(sqlServerDatabases)

//Resources
resource logAnalyticsWorkspace 'Microsoft.OperationalInsights/workspaces@2020-08-01' existing = {
  name: logAnalytics001Name
}

resource datafactoryworkspace 'Microsoft.DataFactory/factories@2018-06-01' existing = {
  name: datafactoryName
}

resource openAIInstance 'Microsoft.CognitiveServices/accounts@2023-05-01' existing = {
  name: openAiName
}

resource sqlServer 'Microsoft.Sql/servers@2020-11-01-preview' existing = {
  name: sqlServerName
}

resource sqlDatabases 'Microsoft.Sql/servers/databases@2020-11-01-preview' existing = [for sqlDatabase in sqlServerDatabases: {
  parent: sqlServer
  name: sqlDatabase
}]

resource mySqlServer 'Microsoft.DBForMySQL/servers@2017-12-01' existing = {
  name: mysql001Name
}

resource mariaDBServer 'Microsoft.DBForMariaDB/servers@2018-06-01' existing = {
  name: mariadb001Name
}

resource postgreSQLServer 'Microsoft.DBForPostgreSQL/servers@2017-12-01' existing = {
  name: potsgresql001Name
}

resource cosmosDB 'Microsoft.DocumentDB/databaseAccounts@2021-03-15' existing = {
  name: cosmosdb001Name
}

// resource databricks 'Microsoft.Databricks/workspaces@2021-04-01-preview' existing = {
//   name: databricksName
// } 

// Diagnostic settings for Azure Data Factory.
resource diagnosticSetting001 'Microsoft.Insights/diagnosticSettings@2021-05-01-preview' = if (enableDataFactory) {
  scope: datafactoryworkspace
  name: 'diagnostic-${datafactoryworkspace.name}'
  properties: {
    workspaceId: logAnalyticsWorkspace.id
    logs: [
      {
        category: 'PipelineRuns'
        enabled: true
      }
      {
        category: 'TriggerRuns'
        enabled: true
      }
      {
        category: 'ActivityRuns'
        enabled: true
      }
    ]
    metrics: [
      {
        category: 'AllMetrics'
        enabled: true
      }
    ]
  }
}



// Diagnostic settings for Azure SQL Server.
resource diagnosticSetting005 'Microsoft.Insights/diagnosticSettings@2021-05-01-preview' = [for i in range(0, sqlServerDatabasesCount): if (sqlFlavour == 'mysql') {
  scope: sqlDatabases[i]
  name: 'diagnostic-${sqlDatabases[i].name}'
  properties: {
    workspaceId: logAnalyticsWorkspace.id
    logs: [
      {
        category: 'SQLInsights'
        enabled: true
      }
      {
        category: 'Errors'
        enabled: true
      }
      {
        category: 'Timeouts'
        enabled: true
      }
    ]
    metrics: [
      {
        category: 'Basic'
        enabled: true
      }
    ]
  }
}]

// Diagnostic settings for Azure Database for MySQL Server.
resource diagnosticSetting006 'Microsoft.Insights/diagnosticSettings@2021-05-01-preview' = if (sqlFlavour == 'mysql') {
  scope: mySqlServer
  name: 'diagnostic-${mySqlServer.name}'
  properties: {
    workspaceId: logAnalyticsWorkspace.id
    logs: [
      {
        category: 'MySqlSlowLogs'
        enabled: true
      }
      {
        category: 'MySqlAuditLogs'
        enabled: true
      }
    ]
    metrics: [
      {
        category: 'AllMetrics'
        enabled: true
      }
    ]
  }
}

// Diagnostic settings for Azure Database for MariaDB Server.
resource diagnosticSetting007 'Microsoft.Insights/diagnosticSettings@2021-05-01-preview' = if (sqlFlavour == 'maria') {
  scope: mariaDBServer
  name: 'diagnostic-${mariaDBServer.name}'
  properties: {
    workspaceId: logAnalyticsWorkspace.id
    logs: [
      {
        category: 'MySqlSlowLogs'
        enabled: true
      }
      {
        category: 'MySqlAuditLogs'
        enabled: true
      }
    ]
    metrics: [
      {
        category: 'AllMetrics'
        enabled: true
      }
    ]
  }
}

// Diagnostic settings for Azure Database for PostgreSQL.
resource diagnosticSetting008 'Microsoft.Insights/diagnosticSettings@2021-05-01-preview' = if (sqlFlavour == 'postgre') {
  scope: postgreSQLServer
  name: 'diagnostic-${postgreSQLServer.name}'
  properties: {
    workspaceId: logAnalyticsWorkspace.id
    logs: [
      {
        category: 'PostgreSQLLogs'
        enabled: true
      }
      {
        category: 'QueryStoreRuntimeStatistics'
        enabled: true
      }
      {
        category: 'QueryStoreWaitStatistics'
        enabled: true
      }
    ]
    metrics: [
      {
        category: 'AllMetrics'
        enabled: true
      }
    ]
  }
}

// Diagnostic settings for Azure Cosmos DB.
resource diagnosticSetting009 'Microsoft.Insights/diagnosticSettings@2021-05-01-preview' = if (enableCosmos) {
  scope: cosmosDB
  name: 'diagnostic-${cosmosDB.name}'
  properties: {
    workspaceId: logAnalyticsWorkspace.id
    logs: [
      {
        category: 'DataPlaneRequests'
        enabled: true
      }
      {
        category: 'ControlPlaneRequests'
        enabled: true
      }
    ]
    metrics: [
      {
        category: 'Requests'
        enabled: true
      }
    ]
  }
}

resource diagnosticSetting010 'Microsoft.Insights/diagnosticSettings@2021-05-01-preview' = if (enableOpenAi) {
  scope: openAIInstance
  name: 'diagnostic-${openAIInstance.name}'
  properties: {
    workspaceId: logAnalyticsWorkspace.id
    logs: [
      {
        category: null
        categoryGroup: 'allLogs'
        enabled: true
        retentionPolicy: {
          days: 0
          enabled: false
        }
      }
    ]
    metrics: [
      {
        timeGrain: null
        enabled: true
        retentionPolicy: {
          days: 0
          enabled: false
        }
        category: 'AllMetrics'
      }
    ]
  }
}

// resource diagnosticSetting011 'Microsoft.Insights/diagnosticSettings@2021-05-01-preview' = {
//   scope: databricks
//   name: 'diagnostic-${databricks.name}'
//   properties: {
//     workspaceId: logAnalyticsWorkspace.id
//     logs: [
//       {
//         category: null
//         categoryGroup: 'allLogs'
//         enabled: true
//         retentionPolicy: {
//           days: 0
//           enabled: false
//         }
//       }
//     ]
//   }
// }
//Outputs
