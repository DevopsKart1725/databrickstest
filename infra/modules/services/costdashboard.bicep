// This template is used to create a dashboard.
targetScope = 'resourceGroup'

// Parameters
param location string
param dashboardName string
param tags object
param resourceGroupName string
param subscriptionId string
param environment string

@description('Name of the dashboard to display in Azure portal')
param dashboardDisplayName string = 'Cost-${dashboardName}-${environment}'

resource dashboard 'Microsoft.Portal/dashboards@2020-09-01-preview' = {
  name: dashboardDisplayName
  location: location
  tags: {
    'hidden-title': dashboardDisplayName
  }
  properties: {
    lenses: [
      {
        order: 0
        parts: [
          {
            position: {
              x: 0
              y: 0
              colSpan: 4
              rowSpan: 4
            }
            metadata: {
              inputs: []
              type: 'Extension/HubsExtension/PartType/MarkdownPart'
              settings: {
                content: {
                  settings:{
                    content: 'This Dashboard helps to visualize how the platform behaves and is being used. A series of diagrams around usage, and costs, have been created to enable observability for stakeholders.\n\n* __Accumulated Costs Dashboard - Last 30 Days__\n\n\tCosts asociated with the Data Product - Accumulated - Last 30 Days\n\n* __Daily Costs Dashboard - Last 24 Hours__\n\n\tCosts asociated with the Data Product - Accumulated - Last 24 Hours\n'
                    title: 'Costs Analysis'
                    subtitle: 'Costs asociated with the Data Product'
                    markdownSource: 1
                    markdownUri: ''   
                    }   
                  }  
                }
              }
              // title: 'Costs Analysis'
              // subtitle: 'Costs asociated with the Data Product'
             }
          {
            position: {
              x: 4
              y: 0
              colSpan: 6
              rowSpan: 4
            }
            metadata: {
              inputs: [
                {
                  name: 'scope'
                  value: '/subscriptions/${subscriptionId}/resourceGroups/${resourceGroupName}'
                }
                {
                  name: 'scopeName'
                  value: 'Costs associated with the Data Product - Accumulated - Last 30 Days' 
                }
                {
                  name: 'view'
                  value: {
                    currency: 'USD'
                    dateRange: 'Last30Days'
                    query: {
                      type: 'ActualCost'
                      dataSet: {
                        granularity: 'Daily'
                        aggregation: {
                          totalCost: {
                            name: 'Cost'
                            function: 'Sum'
                          }
                          totalCostUSD: {
                            name: 'CostUSD'
                            function: 'Sum'
                          }
                        }
                        sorting: [
                          {
                            direction: 'ascending'
                            name: 'UsageDate'
                          }
                        ]
                        grouping: [
                          {
                            type: 'Dimension'
                            name: 'ResourceType'
                          }
                        ]
                      }
                      timeframe: 'None'
                    }
                    chart: 'Area'
                    accumulated: 'true'
                    pivots: [
                      {
                        type: 'Dimension'
                        name: 'ServiceName'
                      }
                      {
                        type: 'Dimension'
                        name: 'ResourceLocation'
                      }
                      {
                        type: 'Dimension'
                        name: 'ResourceId'
                      }
                    ]
                    scope: 'subscriptions/${subscriptionId}/resourceGroups/${resourceGroupName}'
                    kpis: [
                      {
                        type: 'Budget'
                        id: 'COST_NAVIGATOR.BUDGET_OPTIONS.NONE'
                        enabled: true
                        extendedProperties: {
                          name: 'COST_NAVIGATOR.BUDGET_OPTIONS.NONE'
                        }
                      }
                      {
                        type: 'Forecast'
                        enabled: true
                      }
                    ]
                    displayName: 'Accumulated Costs - Dashboard'
                  }
                  isOptional: true
                }
                {
                  name: 'externalState'
                  isOptional: true
                }
              ]
              type: 'Extension/Microsoft_Azure_CostManagement/PartType/CostAnalysisPinPart'
              deepLink: '#@synh.onmicrosoft.com/resource/subscriptions/${subscriptionId}/resourceGroups/${resourceGroupName}/costanalysis'
              title: 'Accumulated Costs - Dashboard'
              subtitle: 'Costs associated with the Data Product - Accumulated - Last 30 Days'
            }
          }
          {
            position: {
              x: 10
              y: 0
              colSpan: 6
              rowSpan: 4
            }
            metadata: {
              inputs: [
                {
                  name: 'scope'
                  value: '/subscriptions/${subscriptionId}/resourceGroups/${resourceGroupName}'
                }
                {
                  name: 'scopeName'
                  value: 'Costs associated with the Data Product - Daily - Last 24 hours'
                }
                {
                  name: 'view'
                  value: {
                    currency: 'USD'
                    dateRange: 'Last30Days'
                    query: {
                      type: 'ActualCost'
                      dataSet: {
                        granularity: 'Daily'
                        aggregation: {
                          totalCost: {
                            name: 'Cost'
                            function: 'Sum'
                          }
                          totalCostUSD: {
                            name: 'CostUSD'
                            function: 'Sum'
                          }
                        }
                        sorting: [
                          {
                            direction: 'ascending'
                            name: 'UsageDate'
                          }
                        ]
                        grouping: [
                          {
                            type: 'Dimension'
                            name: 'ResourceType'
                          }
                        ]
                      }
                      timeframe: 'None'
                    }
                    chart: 'StackedColumn'
                    accumulated: 'false'
                    pivots: [
                      {
                        type: 'Dimension'
                        name: 'ServiceName'
                      }
                      {
                        type: 'Dimension'
                        name: 'ResourceLocation'
                      }
                      {
                        type: 'Dimension'
                        name: 'ResourceId'
                      }
                    ]
                    scope: 'subscriptions/${subscriptionId}/resourceGroups/${resourceGroupName}'
                    kpis: [
                      {
                        type: 'Budget'
                        id: 'COST_NAVIGATOR.BUDGET_OPTIONS.NONE'
                        enabled: true
                        extendedProperties: {
                          name: 'COST_NAVIGATOR.BUDGET_OPTIONS.NONE'
                        }
                      }
                      {
                        type: 'Forecast'
                        enabled: true
                      }
                    ]
                    displayName: 'Daily Costs - Dashboard'
                  }
                  isOptional: true
                }
                {
                  name: 'externalState'
                  isOptional: true
                }
              ]
              type: 'Extension/Microsoft_Azure_CostManagement/PartType/CostAnalysisPinPart'
              deepLink: '#@synh.onmicrosoft.com/resource/subscriptions/${subscriptionId}/resourceGroups/${resourceGroupName}/costanalysis'
              title: 'Daily Costs - Dashboard'
              subtitle: 'Costs associated with the Data Product - Daily - Last 24 hours'
             }
          }
        ]
      }
   ]
    metadata: {
      model: {
        timeRange: {
          value: {
            relative: {
              duration: 24
              timeUnit: 1
            }
          }
          type: 'MsPortalFx.Composition.Configuration.ValueTypes.TimeRange'
        }
      
        filterLocale: {
          value: 'en-us'
        }
        filters: {
          value: {
            MsPortalFx_TimeRange: {
              model: {
                format: 'utc'
                granularity: 'auto'
                relative: '24h'
              }
              displayCache: {
                name: 'UTC Time'
                value: 'Past 24 hours'
              }
              filteredPartIds: []
            }
          }
        }
      }
    }
  }
}
//name: 'Citeline Dashboard'
//  type: 'Microsoft.Portal/dashboards'
//  location: 'INSERT LOCATION'
//  tags: {
//    hidden-title: 'Citeline Dashboard'
//  }
//  apiVersion: '2015-08-01-preview'
//}
