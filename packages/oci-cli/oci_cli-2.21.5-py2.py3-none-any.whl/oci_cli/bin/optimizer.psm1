function GetOciTopLevelCommand_optimizer() {
    return 'optimizer'
}

function GetOciSubcommands_optimizer() {
    $ociSubcommands = @{
        'optimizer' = 'category category-summary enrollment-status enrollment-status-summary history-summary profile profile-summary recommendation recommendation-strategy-summary recommendation-summary resource-action resource-action-summary work-request work-request-error work-request-log-entry'
        'optimizer category' = 'get'
        'optimizer category-summary' = 'list'
        'optimizer enrollment-status' = 'get update'
        'optimizer enrollment-status-summary' = 'list'
        'optimizer history-summary' = 'list'
        'optimizer profile' = 'create delete get update'
        'optimizer profile-summary' = 'list'
        'optimizer recommendation' = 'bulk-apply get update'
        'optimizer recommendation-strategy-summary' = 'list-recommendation-strategies'
        'optimizer recommendation-summary' = 'list'
        'optimizer resource-action' = 'get update'
        'optimizer resource-action-summary' = 'list'
        'optimizer work-request' = 'get list'
        'optimizer work-request-error' = 'list'
        'optimizer work-request-log-entry' = 'list'
    }
    return $ociSubcommands
}

function GetOciCommandsToLongParams_optimizer() {
    $ociCommandsToLongParams = @{
        'optimizer category get' = 'category-id from-json help'
        'optimizer category-summary list' = 'all compartment-id compartment-id-in-subtree from-json help lifecycle-state limit name page page-size sort-by sort-order'
        'optimizer enrollment-status get' = 'enrollment-status-id from-json help'
        'optimizer enrollment-status update' = 'enrollment-status-id from-json help if-match max-wait-seconds status wait-for-state wait-interval-seconds'
        'optimizer enrollment-status-summary list' = 'all compartment-id from-json help lifecycle-state limit page page-size sort-by sort-order status'
        'optimizer history-summary list' = 'all compartment-id compartment-id-in-subtree from-json help lifecycle-state limit name page page-size recommendation-id recommendation-name resource-type sort-by sort-order status'
        'optimizer profile create' = 'compartment-id defined-tags description freeform-tags from-json help levels-configuration max-wait-seconds name target-compartments target-tags wait-for-state wait-interval-seconds'
        'optimizer profile delete' = 'force from-json help if-match max-wait-seconds profile-id wait-for-state wait-interval-seconds'
        'optimizer profile get' = 'from-json help profile-id'
        'optimizer profile update' = 'defined-tags description force freeform-tags from-json help if-match levels-configuration max-wait-seconds name profile-id target-compartments target-tags wait-for-state wait-interval-seconds'
        'optimizer profile-summary list' = 'all compartment-id from-json help lifecycle-state limit name page page-size sort-by sort-order'
        'optimizer recommendation bulk-apply' = 'actions from-json help max-wait-seconds recommendation-id resource-action-ids status time-status-end wait-for-state wait-interval-seconds'
        'optimizer recommendation get' = 'from-json help recommendation-id'
        'optimizer recommendation update' = 'from-json help if-match max-wait-seconds recommendation-id status time-status-end wait-for-state wait-interval-seconds'
        'optimizer recommendation-strategy-summary list-recommendation-strategies' = 'all compartment-id compartment-id-in-subtree from-json help limit name page page-size recommendation-name sort-by sort-order'
        'optimizer recommendation-summary list' = 'all category-id compartment-id compartment-id-in-subtree from-json help lifecycle-state limit name page page-size sort-by sort-order status'
        'optimizer resource-action get' = 'from-json help resource-action-id'
        'optimizer resource-action update' = 'from-json help if-match max-wait-seconds resource-action-id status time-status-end wait-for-state wait-interval-seconds'
        'optimizer resource-action-summary list' = 'all compartment-id compartment-id-in-subtree from-json help lifecycle-state limit name page page-size recommendation-id resource-type sort-by sort-order status'
        'optimizer work-request get' = 'from-json help work-request-id'
        'optimizer work-request list' = 'all compartment-id from-json help limit page page-size'
        'optimizer work-request-error list' = 'all from-json help limit page page-size work-request-id'
        'optimizer work-request-log-entry list' = 'all from-json help limit page page-size work-request-id'
    }
    return $ociCommandsToLongParams
}

function GetOciCommandsToShortParams_optimizer() {
    $ociCommandsToShortParams = @{
        'optimizer category get' = '? h'
        'optimizer category-summary list' = '? c h'
        'optimizer enrollment-status get' = '? h'
        'optimizer enrollment-status update' = '? h'
        'optimizer enrollment-status-summary list' = '? c h'
        'optimizer history-summary list' = '? c h'
        'optimizer profile create' = '? c h'
        'optimizer profile delete' = '? h'
        'optimizer profile get' = '? h'
        'optimizer profile update' = '? h'
        'optimizer profile-summary list' = '? c h'
        'optimizer recommendation bulk-apply' = '? h'
        'optimizer recommendation get' = '? h'
        'optimizer recommendation update' = '? h'
        'optimizer recommendation-strategy-summary list-recommendation-strategies' = '? c h'
        'optimizer recommendation-summary list' = '? c h'
        'optimizer resource-action get' = '? h'
        'optimizer resource-action update' = '? h'
        'optimizer resource-action-summary list' = '? c h'
        'optimizer work-request get' = '? h'
        'optimizer work-request list' = '? c h'
        'optimizer work-request-error list' = '? h'
        'optimizer work-request-log-entry list' = '? h'
    }
    return $ociCommandsToShortParams
}