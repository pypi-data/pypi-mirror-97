function GetOciTopLevelCommand_organizations() {
    return 'organizations'
}

function GetOciSubcommands_organizations() {
    $ociSubcommands = @{
        'organizations' = 'link recipient-invitation sender-invitation work-request work-request-error work-request-log-entry'
        'organizations link' = 'delete get list'
        'organizations recipient-invitation' = 'accept get ignore list update'
        'organizations sender-invitation' = 'cancel create get list update'
        'organizations work-request' = 'get list'
        'organizations work-request-error' = 'list'
        'organizations work-request-log-entry' = 'list'
    }
    return $ociSubcommands
}

function GetOciCommandsToLongParams_organizations() {
    $ociCommandsToLongParams = @{
        'organizations link delete' = 'force from-json help if-match link-id max-wait-seconds wait-for-state wait-interval-seconds'
        'organizations link get' = 'from-json help link-id'
        'organizations link list' = 'all child-tenancy-id from-json help lifecycle-state limit page page-size parent-tenancy-id sort-order'
        'organizations recipient-invitation accept' = 'from-json help if-match max-wait-seconds recipient-invitation-id wait-for-state wait-interval-seconds'
        'organizations recipient-invitation get' = 'from-json help recipient-invitation-id'
        'organizations recipient-invitation ignore' = 'from-json help if-match max-wait-seconds recipient-invitation-id wait-for-state wait-interval-seconds'
        'organizations recipient-invitation list' = 'all compartment-id from-json help lifecycle-state page sender-tenancy-id status'
        'organizations recipient-invitation update' = 'defined-tags display-name force freeform-tags from-json help if-match max-wait-seconds recipient-invitation-id wait-for-state wait-interval-seconds'
        'organizations sender-invitation cancel' = 'from-json help if-match max-wait-seconds sender-invitation-id wait-for-state wait-interval-seconds'
        'organizations sender-invitation create' = 'compartment-id defined-tags display-name freeform-tags from-json help max-wait-seconds recipient-email-address recipient-tenancy-id wait-for-state wait-interval-seconds'
        'organizations sender-invitation get' = 'from-json help sender-invitation-id'
        'organizations sender-invitation list' = 'all compartment-id display-name from-json help lifecycle-state limit page page-size recipient-tenancy-id sort-by sort-order status'
        'organizations sender-invitation update' = 'defined-tags display-name force freeform-tags from-json help if-match max-wait-seconds sender-invitation-id wait-for-state wait-interval-seconds'
        'organizations work-request get' = 'from-json help work-request-id'
        'organizations work-request list' = 'all compartment-id from-json help limit page page-size sort-order'
        'organizations work-request-error list' = 'all compartment-id from-json help limit page page-size sort-order work-request-id'
        'organizations work-request-log-entry list' = 'all compartment-id from-json help limit page page-size sort-order work-request-id'
    }
    return $ociCommandsToLongParams
}

function GetOciCommandsToShortParams_organizations() {
    $ociCommandsToShortParams = @{
        'organizations link delete' = '? h'
        'organizations link get' = '? h'
        'organizations link list' = '? h'
        'organizations recipient-invitation accept' = '? h'
        'organizations recipient-invitation get' = '? h'
        'organizations recipient-invitation ignore' = '? h'
        'organizations recipient-invitation list' = '? c h'
        'organizations recipient-invitation update' = '? h'
        'organizations sender-invitation cancel' = '? h'
        'organizations sender-invitation create' = '? c h'
        'organizations sender-invitation get' = '? h'
        'organizations sender-invitation list' = '? c h'
        'organizations sender-invitation update' = '? h'
        'organizations work-request get' = '? h'
        'organizations work-request list' = '? c h'
        'organizations work-request-error list' = '? c h'
        'organizations work-request-log-entry list' = '? c h'
    }
    return $ociCommandsToShortParams
}