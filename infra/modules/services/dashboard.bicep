// Copyright (c) Microsoft Corporation.
// Licensed under the MIT license.

// This template is used to create a dashboard.
targetScope = 'resourceGroup'

// Parameters
param location string
param dashboardName string
param tags object
param datafactoryScope string
param datafactoryName string
param enableDataFactory bool
param enableOpenAi bool
param openAiAcope string
@description('Name of the dashboard to display in Azure portal')
param openAiDashboardDisplayName string = '${dashboardName}-OpenAI'
//? param processingService string
//param synapseScope string
//param synapse001Name string

// Variables

// Resources
resource dashboardDataFactory 'Microsoft.Portal/dashboards@2020-09-01-preview' = if (enableDataFactory) {
  name: '${dashboardName}-dataFactory'
  location: location
  tags: tags
  properties: {
    lenses: [
      {
        order: 0
        parts: [
          {
            position: {
              x: 0
              y: 0
              rowSpan: 4
              colSpan: 6
            }
            metadata: {
              inputs: [
                {
                  name: 'options'
                  isOptional: true
                }
                {
                  name: 'sharedTimeRange'
                  isOptional: true
                }
              ]
              type: 'Extension/HubsExtension/PartType/MonitorChartPart'
              settings: {
                content: {
                  options: {
                    chart: {
                      metrics: [
                        {
                          resourceMetadata: {
                            id: datafactoryScope
                          }
                          name: 'PipelineFailedRuns'
                          aggregationType: 1
                          namespace: 'microsoft.datafactory/factories'
                          metricVisualization: {
                            displayName: 'Failed pipeline runs metrics'
                            resourceDisplayName: datafactoryName
                          }
                        }
                      ]
                      title: 'Count Failed activity runs metrics for ${datafactoryName}'
                      titleKind: 1
                      visualization: {
                        chartType: 2
                        legendVisualization: {
                          isVisible: true
                          position: 2
                          hideSubtitle: false
                        }
                        axisVisualization: {
                          x: {
                            isVisible: true
                            axisType: 2
                          }
                          y: {
                            isVisible: true
                            axisType: 1
                          }
                        }
                        disablePinning: true
                      }
                    }
                  }
                }
              }
            }
          }
          {
            position: {
              x: 6
              y: 0
              rowSpan: 4
              colSpan: 6
            }
            metadata: {
              inputs: [
                {
                  name: 'options'
                  isOptional: true
                }
                {
                  name: 'sharedTimeRange'
                  isOptional: true
                }
              ]
              type: 'Extension/HubsExtension/PartType/MonitorChartPart'
              settings: {
                content: {
                  options: {
                    chart: {
                      metrics: [
                        {
                          resourceMetadata: {
                            id: datafactoryScope
                          }
                          name: 'PipelineSucceededRuns'
                          aggregationType: 1
                          namespace: 'microsoft.datafactory/factories'
                          metricVisualization: {
                            displayName: 'Succeeded pipeline runs metrics'
                            resourceDisplayName: datafactoryName
                          }
                        }
                      ]
                      title: 'Sum Succeeded pipeline runs metrics for ${datafactoryName}'
                      titleKind: 1
                      visualization: {
                        chartType: 2
                        legendVisualization: {
                          isVisible: true
                          position: 2
                          hideSubtitle: false
                        }
                        axisVisualization: {
                          x: {
                            isVisible: true
                            axisType: 2
                          }
                          y: {
                            isVisible: true
                            axisType: 1
                          }
                        }
                        disablePinning: true
                      }
                    }
                  }
                }
              }
            }
          }
        ]
      }
    ]
    metadata: {
      model: {}
    }
  }
}

// OpenAI Metrics Dashboard
resource dashboardOpenAi 'Microsoft.Portal/dashboards@2020-09-01-preview' = if (enableOpenAi) {
  name: openAiDashboardDisplayName
  location: location
  tags: {
    'hidden-title': openAiDashboardDisplayName
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
              rowSpan: 6
            }
            metadata: {
              inputs: []
              type: 'Extension/HubsExtension/PartType/MarkdownPart'
              settings: {
                content: {
                  settings:{
                    content: 'This Dashboard helps to visualize how the platform behaves and is being used. A series of diagrams around usage, and costs, have been created to enable observability for stakeholders. \n\n* __Azure OpenAI Tokens/Requests - Last 24 Hours__\n\n\tAzure OpenAI Tokens/Requests - Accumulated - Last 24 Hours\n\t\n\t_RateLimit_: The current ratelimit of the ratelimit key.\n\n\t_Generated Completion Tokens_: Number of Generated Tokens that are output by an AI model after processing an initial prompt. Tokens in the text created by the AI model\n\n\t_Processed Prompt Tokens_: Number of Prompt Tokens that make up the initial prompt provided by the user. These represent the input to the model.\n\n\t_Processed Inference Tokens_: Number of Tokens that are actually generated by the model as output. \n\tThis includes the prompt tokens plus any additional generated text. Tokens fed into the model after processing'
                    title: 'OpenAI Metrics'
                    subtitle: 'Metrics asociated with the OpenAI Token and Requests'
                    markdownSource: 1
                    markdownUri: ''   
                  }
                }  
              }
            }
          }
          {
            position: {
              x: 4
              y: 0
              colSpan: 11
              rowSpan: 6
            }
            metadata: {
              inputs: [
                {
                  name: 'options'
                  value: {
                    chart: {
                      metrics: [
                        {
                          resourceMetadata: {
                            id: openAiAcope
                          }
                          name: 'GeneratedTokens'
                          aggregationType: 1
                          namespace: 'microsoft.cognitiveservices/accounts'
                          metricVisualization: {
                            displayName: 'Generated Completion Tokens'
                          }
                        }
                        {
                          resourceMetadata: {
                            id: openAiAcope
                          }
                          name: 'Ratelimit'
                          aggregationType: 1
                          namespace: 'microsoft.cognitiveservices/accounts'
                          metricVisualization: {
                            displayName: 'Ratelimit'
                          }
                        }
                        {
                          resourceMetadata: {
                            id: openAiAcope
                          }
                          name: 'ProcessedPromptTokens'
                          aggregationType: 1
                          namespace: 'microsoft.cognitiveservices/accounts'
                          metricVisualization: {
                            displayName: 'Processed Prompt Tokens'
                          }
                        }
                        {
                          resourceMetadata: {
                            id: openAiAcope
                          }
                          name: 'TokenTransaction'
                          aggregationType: 1
                          namespace: 'microsoft.cognitiveservices/accounts'
                          metricVisualization: {
                            displayName: 'Processed Inference Tokens'
                          }
                        }
                      ]
                      title: 'Azure OpenAI Tokens/Requests Accumulated - Last 24 hours'
                      titleKind: 1
                      visualization: {
                        chartType: 2
                        legendVisualization: {
                          isVisible: true
                          position: 2
                          hideSubtitle: false
                        }
                        axisVisualization: {
                          x: {
                            isVisible: true
                            axisType: 2
                          }
                          y: {
                            isVisible: true
                            axisType: 1
                          }
                        }
                      }
                      timespan: {
                        relative: {
                          duration: 86400000
                        }
                        showUTCTime: false
                        grain: 1
                      }
                    }
                  }
                  isOptional: true
                }
                {
                  name: 'sharedTimeRange'
                  isOptional: true
                }
              ]
              type: 'Extension/HubsExtension/PartType/MonitorChartPart'
              settings: {
                content: {
                  options: {
                    chart: {
                      metrics: [
                        {
                          resourceMetadata: {
                            id: openAiAcope
                          }
                          name: 'GeneratedTokens'
                          aggregationType: 1
                          namespace: 'microsoft.cognitiveservices/accounts'
                          metricVisualization: {
                            displayName: 'Generated Completion Tokens'
                          }
                        }
                        {
                          resourceMetadata: {
                            id: openAiAcope
                          }
                          name: 'Ratelimit'
                          aggregationType: 1
                          namespace: 'microsoft.cognitiveservices/accounts'
                          metricVisualization: {
                            displayName: 'Ratelimit'
                          }
                        }
                        {
                          resourceMetadata: {
                            id: openAiAcope
                          }
                          name: 'ProcessedPromptTokens'
                          aggregationType: 1
                          namespace: 'microsoft.cognitiveservices/accounts'
                          metricVisualization: {
                            displayName: 'Processed Prompt Tokens'
                          }
                        }
                        {
                          resourceMetadata: {
                            id: openAiAcope
                          }
                          name: 'TokenTransaction'
                          aggregationType: 1
                          namespace: 'microsoft.cognitiveservices/accounts'
                          metricVisualization: {
                            displayName: 'Processed Inference Tokens'
                          }
                        }
                      ]
                      title: 'Azure OpenAI Tokens/Requests Accumulated - Last 24 hours'
                      titleKind: 2
                      visualization: {
                        chartType: 2
                        legendVisualization: {
                          isVisible: true
                          position: 2
                          hideSubtitle: false
                        }
                        axisVisualization: {
                          x: {
                            isVisible: true
                            axisType: 2
                          }
                          y: {
                            isVisible: true
                            axisType: 1
                          }
                        }
                        disablePinning: true
                      }
                    }
                  }
                }
              }
              filters: {
                MsPortalFx_TimeRange: {
                  model: {
                    format: 'local'
                    granularity: 'auto'
                    relative: '1440m'
                  }
                }
              }
            }
          }
        ]
      }
    ]
    metadata: {
      model: {}
    }
  }
}

// Outputs
