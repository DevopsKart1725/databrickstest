$scriptPath = split-path -parent $MyInvocation.MyCommand.Definition

$jsonDevParams = (Get-Content "$scriptPath/../params.dev.json" -Raw) | ConvertFrom-Json
$PROJECT_NAME = $jsonDevParams.psobject.properties.Value.prefix.Value

$DevParameters = @{
    environment           = "dev"
    projectName           = $PROJECT_NAME
    armServiceConnnection = "IEP-LANDING-DEV-AzureDevOpsPipelineSP"
    azureSubscription     = "d9f56f19-917a-4893-883e-1a93932f741b"
    dataFactoryName       = "$PROJECT_NAME-dev-datafactory001"
    amlWorkspaceName      = "$PROJECT_NAME-dev-machinelearning001"
    resourceGroupName     = "iepdlz01-dev-$PROJECT_NAME"
}

$StagingParameters = @{
    environment           = "stg"
    projectName           = $PROJECT_NAME
    armServiceConnnection = "IEP-LANDING-STG-AzureDevOpsPipelineSP"
    azureSubscription     = "8e170088-cdc4-4bef-9572-bc278956701e"
    dataFactoryName       = "$PROJECT_NAME-stg-datafactory001"
    amlWorkspaceName      = "$PROJECT_NAME-stg-machinelearning001"
    resourceGroupName     = "iepdlz01-stg-$PROJECT_NAME"
}

& "$scriptPath/new-variable-group.ps1" @DevParameters
& "$scriptPath/new-variable-group.ps1" @StagingParameters