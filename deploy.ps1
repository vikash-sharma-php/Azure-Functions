$ErrorActionPreference = 'Stop'
# Connect-AzAccount
func.cmd azure functionapp publish algobot --build remote --nozip --build-native-deps
# --publish-local-settings