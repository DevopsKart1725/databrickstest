# az account list -o table
# az account set --subscription "SYNH-EUSDEV-CR-IEPDATA-LANDING"

$projectName="demo-friday"

# Delete a RG
$resourceGroupName="$projectName-rg"
az group delete --name  $resourceGroupName

# Delete Subnet
$vnetResourceGroup="iepdlz01-dev-network"
$vnetName="iepdlz01-dev-vnet"
$snetName="$projectName-snet"


az network vnet subnet delete -g $vnetResourceGroup --vnet-name $vnetName -n $snetName
