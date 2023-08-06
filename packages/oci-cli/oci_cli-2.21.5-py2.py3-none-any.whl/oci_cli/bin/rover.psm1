function GetOciTopLevelCommand_rover() {
    return 'rover'
}

function GetOciSubcommands_rover() {
    $ociSubcommands = @{
        'rover' = 'cluster node'
        'rover cluster' = 'add-workload change-compartment create delete delete-workload list list-workload request-approval set-secrets show update'
        'rover node' = 'add-workload change-compartment create delete delete-workload get-encryption-key list list-workload request-approval set-secrets show update'
    }
    return $ociSubcommands
}

function GetOciCommandsToLongParams_rover() {
    $ociCommandsToLongParams = @{
        'rover cluster add-workload' = 'bucket-id bucket-name cluster-id compartment-id from-json help image-id prefix range-end range-start type'
        'rover cluster change-compartment' = 'cluster-id compartment-id from-json help if-match'
        'rover cluster create' = 'address1 address2 address3 address4 addressee care-of city-or-locality cluster-size cluster-workloads compartment-id country defined-tags display-name email enclosure-type freeform-tags from-json help lifecycle-state lifecycle-state-details max-wait-seconds oracle-shipping-tracking-url phone-number point-of-contact point-of-contact-phone-number shipping-preference shipping-vendor state-province-region super-user-password system-tags time-pickup-expected unlock-passphrase wait-for-state wait-interval-seconds zip-postal-code'
        'rover cluster delete' = 'cluster-id force from-json help if-match max-wait-seconds wait-for-state wait-interval-seconds'
        'rover cluster delete-workload' = 'cluster-id from-json help'
        'rover cluster list' = 'all compartment-id display-name from-json help lifecycle-state limit page page-size sort-by sort-order'
        'rover cluster list-workload' = 'cluster-id from-json help'
        'rover cluster request-approval' = 'cluster-id from-json help'
        'rover cluster set-secrets' = 'cluster-id help super-user-password unlock-passphrase'
        'rover cluster show' = 'cluster-id from-json help'
        'rover cluster update' = 'address1 address2 address3 address4 addressee care-of city-or-locality cluster-id cluster-size cluster-workloads country defined-tags display-name email enclosure-type force freeform-tags from-json help if-match lifecycle-state lifecycle-state-details max-wait-seconds oracle-shipping-tracking-url phone-number point-of-contact point-of-contact-phone-number shipping-preference shipping-vendor state-province-region super-user-password system-tags time-pickup-expected unlock-passphrase wait-for-state wait-interval-seconds zip-postal-code'
        'rover node add-workload' = 'bucket-id bucket-name compartment-id from-json help image-id node-id prefix range-end range-start type'
        'rover node change-compartment' = 'compartment-id from-json help if-match node-id'
        'rover node create' = 'address1 address2 address3 address4 addressee care-of city-or-locality compartment-id country defined-tags display-name email enclosure-type freeform-tags from-json help lifecycle-state lifecycle-state-details max-wait-seconds oracle-shipping-tracking-url phone-number point-of-contact point-of-contact-phone-number public-key serial-number shipping-preference shipping-vendor state-province-region super-user-password system-tags time-pickup-expected time-return-window-ends time-return-window-starts unlock-passphrase wait-for-state wait-interval-seconds zip-postal-code'
        'rover node delete' = 'force from-json help if-match max-wait-seconds node-id wait-for-state wait-interval-seconds'
        'rover node delete-workload' = 'from-json help node-id'
        'rover node get-encryption-key' = 'from-json help node-id'
        'rover node list' = 'all compartment-id display-name from-json help lifecycle-state limit page page-size sort-by sort-order'
        'rover node list-workload' = 'from-json help node-id'
        'rover node request-approval' = 'from-json help node-id'
        'rover node set-secrets' = 'from-json help node-id super-user-password unlock-passphrase'
        'rover node show' = 'from-json help node-id'
        'rover node update' = 'address1 address2 address3 address4 addressee care-of city-or-locality country defined-tags display-name email enclosure-type force freeform-tags from-json help if-match lifecycle-state lifecycle-state-details max-wait-seconds node-id node-workloads oracle-shipping-tracking-url phone-number point-of-contact point-of-contact-phone-number public-key serial-number shipping-preference shipping-vendor state-province-region super-user-password system-tags time-pickup-expected time-return-window-ends time-return-window-starts unlock-passphrase wait-for-state wait-interval-seconds zip-postal-code'
    }
    return $ociCommandsToLongParams
}

function GetOciCommandsToShortParams_rover() {
    $ociCommandsToShortParams = @{
        'rover cluster add-workload' = '? c h'
        'rover cluster change-compartment' = '? c h'
        'rover cluster create' = '? c h'
        'rover cluster delete' = '? h'
        'rover cluster delete-workload' = '? h'
        'rover cluster list' = '? c h'
        'rover cluster list-workload' = '? h'
        'rover cluster request-approval' = '? h'
        'rover cluster set-secrets' = '? h'
        'rover cluster show' = '? h'
        'rover cluster update' = '? h'
        'rover node add-workload' = '? c h'
        'rover node change-compartment' = '? c h'
        'rover node create' = '? c h'
        'rover node delete' = '? h'
        'rover node delete-workload' = '? h'
        'rover node get-encryption-key' = '? h'
        'rover node list' = '? c h'
        'rover node list-workload' = '? h'
        'rover node request-approval' = '? h'
        'rover node set-secrets' = '? h'
        'rover node show' = '? h'
        'rover node update' = '? h'
    }
    return $ociCommandsToShortParams
}