function GetOciTopLevelCommand_artifacts() {
    return 'artifacts'
}

function GetOciSubcommands_artifacts() {
    $ociSubcommands = @{
        'artifacts' = 'container'
        'artifacts container' = 'configuration image repository'
        'artifacts container configuration' = 'get update'
        'artifacts container image' = 'delete get list remove-version restore'
        'artifacts container repository' = 'change-compartment create delete get list update'
    }
    return $ociSubcommands
}

function GetOciCommandsToLongParams_artifacts() {
    $ociCommandsToLongParams = @{
        'artifacts container configuration get' = 'compartment-id from-json help'
        'artifacts container configuration update' = 'compartment-id from-json help if-match is-repository-created-on-first-push'
        'artifacts container image delete' = 'force from-json help if-match image-id max-wait-seconds wait-for-state wait-interval-seconds'
        'artifacts container image get' = 'from-json help image-id'
        'artifacts container image list' = 'all compartment-id compartment-id-in-subtree display-name from-json help image-id image-version is-versioned lifecycle-state limit page page-size repository-id repository-name sort-by sort-order'
        'artifacts container image remove-version' = 'from-json help if-match image-id image-version'
        'artifacts container image restore' = 'from-json help if-match image-id image-version max-wait-seconds wait-for-state wait-interval-seconds'
        'artifacts container repository change-compartment' = 'compartment-id from-json help if-match repository-id'
        'artifacts container repository create' = 'compartment-id display-name from-json help is-immutable is-public max-wait-seconds readme wait-for-state wait-interval-seconds'
        'artifacts container repository delete' = 'force from-json help if-match max-wait-seconds repository-id wait-for-state wait-interval-seconds'
        'artifacts container repository get' = 'from-json help repository-id'
        'artifacts container repository list' = 'all compartment-id compartment-id-in-subtree display-name from-json help is-public lifecycle-state limit page page-size repository-id sort-by sort-order'
        'artifacts container repository update' = 'force from-json help if-match is-immutable is-public readme repository-id'
    }
    return $ociCommandsToLongParams
}

function GetOciCommandsToShortParams_artifacts() {
    $ociCommandsToShortParams = @{
        'artifacts container configuration get' = '? c h'
        'artifacts container configuration update' = '? c h'
        'artifacts container image delete' = '? h'
        'artifacts container image get' = '? h'
        'artifacts container image list' = '? c h'
        'artifacts container image remove-version' = '? h'
        'artifacts container image restore' = '? h'
        'artifacts container repository change-compartment' = '? c h'
        'artifacts container repository create' = '? c h'
        'artifacts container repository delete' = '? h'
        'artifacts container repository get' = '? h'
        'artifacts container repository list' = '? c h'
        'artifacts container repository update' = '? h'
    }
    return $ociCommandsToShortParams
}