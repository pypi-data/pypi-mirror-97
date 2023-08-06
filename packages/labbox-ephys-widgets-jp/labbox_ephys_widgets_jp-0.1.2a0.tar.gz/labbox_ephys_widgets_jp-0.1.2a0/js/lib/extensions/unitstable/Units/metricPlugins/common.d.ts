/// <reference types="react" />
export interface MetricValue {
    numericValue: number;
    stringValue: string;
    isNumeric: boolean;
}
export interface MetricPlugin {
    type: 'metricPlugin';
    metricName: string;
    columnLabel: string;
    tooltip: string;
    hitherFnName: string;
    metricFnParams: {
        [key: string]: any;
    };
    hitherConfig: {
        useClientCache: boolean;
        job_handler_name?: string;
    };
    component: React.ComponentType<{
        record: any;
    }>;
    development?: boolean;
}
export declare const sortMetricValues: (a: MetricValue, b: MetricValue, sortAscending: boolean) => number;
