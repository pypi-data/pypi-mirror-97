function GetOciTopLevelCommand_database_management() {
    return 'database-management'
}

function GetOciSubcommands_database_management() {
    $ociSubcommands = @{
        'database-management' = 'fleet-health-metrics job job-execution job-run managed-database managed-database-group summary-metrics'
        'database-management fleet-health-metrics' = 'get'
        'database-management job' = 'change-compartment create-sql-job delete get list'
        'database-management job-execution' = 'get list'
        'database-management job-run' = 'get list'
        'database-management managed-database' = 'get list'
        'database-management managed-database-group' = 'add change-compartment create delete get list remove update'
        'database-management summary-metrics' = 'get'
    }
    return $ociSubcommands
}

function GetOciCommandsToLongParams_database_management() {
    $ociCommandsToLongParams = @{
        'database-management fleet-health-metrics get' = 'compare-baseline-time compare-target-time compare-type compartment-id filter-by-database-sub-type filter-by-database-type filter-by-metric-names from-json help managed-database-group-id'
        'database-management job change-compartment' = 'compartment-id from-json help if-match job-id'
        'database-management job create-sql-job' = 'compartment-id database-sub-type description from-json help managed-database-group-id managed-database-id max-wait-seconds name operation-type password result-location role schedule-type sql-text sql-type timeout user-name wait-for-state wait-interval-seconds'
        'database-management job delete' = 'force from-json help if-match job-id max-wait-seconds wait-for-state wait-interval-seconds'
        'database-management job get' = 'from-json help job-id'
        'database-management job list' = 'all compartment-id from-json help id lifecycle-state limit managed-database-group-id managed-database-id name page page-size sort-by sort-order'
        'database-management job-execution get' = 'from-json help job-execution-id'
        'database-management job-execution list' = 'all compartment-id from-json help id job-id limit managed-database-group-id managed-database-id name page page-size sort-by sort-order status'
        'database-management job-run get' = 'from-json help job-run-id'
        'database-management job-run list' = 'all compartment-id from-json help id job-id limit managed-database-group-id managed-database-id name page page-size run-status sort-by sort-order'
        'database-management managed-database get' = 'from-json help managed-database-id'
        'database-management managed-database list' = 'all compartment-id from-json help id limit name page page-size sort-by sort-order'
        'database-management managed-database-group add' = 'from-json help managed-database-group-id managed-database-id'
        'database-management managed-database-group change-compartment' = 'compartment-id from-json help if-match managed-database-group-id'
        'database-management managed-database-group create' = 'compartment-id description from-json help max-wait-seconds name wait-for-state wait-interval-seconds'
        'database-management managed-database-group delete' = 'force from-json help if-match managed-database-group-id max-wait-seconds wait-for-state wait-interval-seconds'
        'database-management managed-database-group get' = 'from-json help managed-database-group-id'
        'database-management managed-database-group list' = 'all compartment-id from-json help id lifecycle-state limit name page page-size sort-by sort-order'
        'database-management managed-database-group remove' = 'from-json help managed-database-group-id managed-database-id'
        'database-management managed-database-group update' = 'description from-json help if-match managed-database-group-id max-wait-seconds wait-for-state wait-interval-seconds'
        'database-management summary-metrics get' = 'end-time from-json help managed-database-id start-time'
    }
    return $ociCommandsToLongParams
}

function GetOciCommandsToShortParams_database_management() {
    $ociCommandsToShortParams = @{
        'database-management fleet-health-metrics get' = '? c h'
        'database-management job change-compartment' = '? c h'
        'database-management job create-sql-job' = '? c h'
        'database-management job delete' = '? h'
        'database-management job get' = '? h'
        'database-management job list' = '? c h'
        'database-management job-execution get' = '? h'
        'database-management job-execution list' = '? c h'
        'database-management job-run get' = '? h'
        'database-management job-run list' = '? c h'
        'database-management managed-database get' = '? h'
        'database-management managed-database list' = '? c h'
        'database-management managed-database-group add' = '? h'
        'database-management managed-database-group change-compartment' = '? c h'
        'database-management managed-database-group create' = '? c h'
        'database-management managed-database-group delete' = '? h'
        'database-management managed-database-group get' = '? h'
        'database-management managed-database-group list' = '? c h'
        'database-management managed-database-group remove' = '? h'
        'database-management managed-database-group update' = '? h'
        'database-management summary-metrics get' = '? h'
    }
    return $ociCommandsToShortParams
}