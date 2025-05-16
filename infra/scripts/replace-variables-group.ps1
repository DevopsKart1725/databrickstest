$scriptPath = split-path -parent $MyInvocation.MyCommand.Definition

$jsonDevParams = (Get-Content "$scriptPath/../params.dev.json" -Raw) | ConvertFrom-Json
$PROJECT_NAME = $jsonDevParams.psobject.properties.Value.prefix.Value


$filePath = "$PSScriptRoot\..\..\.ado\workflows"
# Get the files from the folder and iterate using Foreach
Get-ChildItem $filePath -Recurse  -include *.yml | select -expand fullname | ForEach-Object {
    # Read the file and use replace()
    (Get-Content $_) -replace  'dp-dev-variables',"$PROJECT_NAME-dev-variables" | Set-Content $_
    (Get-Content $_) -replace  'dp-stg-variables',"$PROJECT_NAME-stg-variables" | Set-Content $_
    (Get-Content $_) -replace  'dp-prd-variables',"$PROJECT_NAME-prd-variables" | Set-Content $_
}