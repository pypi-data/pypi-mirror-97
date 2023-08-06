function GetOciTopLevelCommand_opsi() {
    return 'opsi'
}

function GetOciSubcommands_opsi() {
    $ociSubcommands = @{
        'opsi' = 'database-insights'
        'opsi database-insights' = 'ingest-sql-bucket ingest-sql-plan-lines ingest-sql-text list list-sql-plans list-sql-searches list-sql-texts summarize-database-insight-resource-capacity-trend summarize-database-insight-resource-forecast-trend summarize-database-insight-resource-statistics summarize-database-insight-resource-usage summarize-database-insight-resource-usage-trend summarize-database-insight-resource-utilization-insight summarize-sql-insights summarize-sql-plan-insights summarize-sql-response-time-distributions summarize-sql-statistics summarize-sql-statistics-time-series summarize-sql-statistics-time-series-by-plan'
    }
    return $ociSubcommands
}

function GetOciCommandsToLongParams_opsi() {
    $ociCommandsToLongParams = @{
        'opsi database-insights ingest-sql-bucket' = 'compartment-id database-id from-json help if-match items'
        'opsi database-insights ingest-sql-plan-lines' = 'compartment-id database-id from-json help if-match items'
        'opsi database-insights ingest-sql-text' = 'compartment-id database-id from-json help if-match items'
        'opsi database-insights list' = 'all compartment-id database-id database-type fields from-json help limit page page-size sort-by sort-order'
        'opsi database-insights list-sql-plans' = 'all compartment-id database-id from-json help page plan-hash sql-identifier'
        'opsi database-insights list-sql-searches' = 'all analysis-time-interval compartment-id from-json help page sql-identifier time-interval-end time-interval-start'
        'opsi database-insights list-sql-texts' = 'all compartment-id database-id from-json help page sql-identifier'
        'opsi database-insights summarize-database-insight-resource-capacity-trend' = 'analysis-time-interval compartment-id database-id database-type from-json help page resource-metric sort-by sort-order time-interval-end time-interval-start utilization-level'
        'opsi database-insights summarize-database-insight-resource-forecast-trend' = 'analysis-time-interval compartment-id confidence database-id database-type forecast-days forecast-model from-json help page resource-metric statistic time-interval-end time-interval-start utilization-level'
        'opsi database-insights summarize-database-insight-resource-statistics' = 'analysis-time-interval compartment-id database-id database-type forecast-days from-json help insight-by limit page percentile resource-metric sort-by sort-order time-interval-end time-interval-start'
        'opsi database-insights summarize-database-insight-resource-usage' = 'analysis-time-interval compartment-id database-id database-type from-json help page percentile resource-metric time-interval-end time-interval-start'
        'opsi database-insights summarize-database-insight-resource-usage-trend' = 'analysis-time-interval compartment-id database-id database-type from-json help page resource-metric sort-by sort-order time-interval-end time-interval-start'
        'opsi database-insights summarize-database-insight-resource-utilization-insight' = 'analysis-time-interval compartment-id database-id database-type forecast-days from-json help page resource-metric time-interval-end time-interval-start'
        'opsi database-insights summarize-sql-insights' = 'analysis-time-interval compartment-id database-id database-time-pct-greater-than database-type from-json help page time-interval-end time-interval-start'
        'opsi database-insights summarize-sql-plan-insights' = 'analysis-time-interval compartment-id database-id from-json help page sql-identifier time-interval-end time-interval-start'
        'opsi database-insights summarize-sql-response-time-distributions' = 'analysis-time-interval compartment-id database-id from-json help page sql-identifier time-interval-end time-interval-start'
        'opsi database-insights summarize-sql-statistics' = 'analysis-time-interval category compartment-id database-id database-time-pct-greater-than database-type from-json help limit page sort-by sort-order sql-identifier time-interval-end time-interval-start'
        'opsi database-insights summarize-sql-statistics-time-series' = 'analysis-time-interval compartment-id database-id from-json help page sql-identifier time-interval-end time-interval-start'
        'opsi database-insights summarize-sql-statistics-time-series-by-plan' = 'analysis-time-interval compartment-id database-id from-json help page sql-identifier time-interval-end time-interval-start'
    }
    return $ociCommandsToLongParams
}

function GetOciCommandsToShortParams_opsi() {
    $ociCommandsToShortParams = @{
        'opsi database-insights ingest-sql-bucket' = '? c h'
        'opsi database-insights ingest-sql-plan-lines' = '? c h'
        'opsi database-insights ingest-sql-text' = '? c h'
        'opsi database-insights list' = '? c h'
        'opsi database-insights list-sql-plans' = '? c h'
        'opsi database-insights list-sql-searches' = '? c h'
        'opsi database-insights list-sql-texts' = '? c h'
        'opsi database-insights summarize-database-insight-resource-capacity-trend' = '? c h'
        'opsi database-insights summarize-database-insight-resource-forecast-trend' = '? c h'
        'opsi database-insights summarize-database-insight-resource-statistics' = '? c h'
        'opsi database-insights summarize-database-insight-resource-usage' = '? c h'
        'opsi database-insights summarize-database-insight-resource-usage-trend' = '? c h'
        'opsi database-insights summarize-database-insight-resource-utilization-insight' = '? c h'
        'opsi database-insights summarize-sql-insights' = '? c h'
        'opsi database-insights summarize-sql-plan-insights' = '? c h'
        'opsi database-insights summarize-sql-response-time-distributions' = '? c h'
        'opsi database-insights summarize-sql-statistics' = '? c h'
        'opsi database-insights summarize-sql-statistics-time-series' = '? c h'
        'opsi database-insights summarize-sql-statistics-time-series-by-plan' = '? c h'
    }
    return $ociCommandsToShortParams
}