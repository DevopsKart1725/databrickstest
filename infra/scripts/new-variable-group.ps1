# az extension add --name azure-devops
Param(
    $environment = $null,
    $projectName = $null,
    $armServiceConnnection = $null,
    $azureSubscription = $null,
    $dataFactoryName = $null,
    $amlWorkspaceName = $null,
    $resourceGroupName = $null
)

#--------------------------------------------

$ADO_ORGANIZATION = "Syneos-IEP-IT-3595"
$ADO_PROJECT = "IEP Data Team"
$ADO_VAR_GROUP_NAME = "$projectName-$environment-variables"

az pipelines variable-group create --name $ADO_VAR_GROUP_NAME `
    --org https://dev.azure.com/$ADO_ORGANIZATION `
    --project $ADO_PROJECT `
    --variables armServiceConnnection=$armServiceConnnection azureSubscription=$azureSubscription `
    dataProductName=$projectName dataFactoryName=$dataFactoryName amlWorkspaceName=$amlWorkspaceName resourceGroupName=$resourceGroupName --output yaml

# az pipelines variable-group variable update --group-id 1 --org https://dev.azure.com/SyneosHealth-CL-DevOps  --project IaC_POC --name app-svc-name --value test1 --output yaml
# az pipelines variable-group list --org https://dev.azure.com/SyneosHealth-CL-DevOps  --project IaC_POC 
