import { Reducer } from "react";
export declare type ExternalSortingUnitMetric = {
    name: string;
    label: string;
    tooltip?: string;
    data: {
        [key: string]: number;
    };
};
declare type SetExternalUnitMetricsAction = {
    type: 'SetExternalUnitMetrics';
    externalUnitMetrics: ExternalSortingUnitMetric[];
};
declare type ExternalUnitMetricsAction = SetExternalUnitMetricsAction;
export declare const externalUnitMetricsReducer: Reducer<ExternalSortingUnitMetric[], ExternalUnitMetricsAction>;
export {};
