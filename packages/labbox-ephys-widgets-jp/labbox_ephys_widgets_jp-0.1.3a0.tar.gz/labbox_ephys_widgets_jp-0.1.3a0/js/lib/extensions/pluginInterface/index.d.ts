import { BasePlugin, CalculationPool, ExtensionContext } from "labbox";
import { FunctionComponent } from "react";
import { RecordingViewPlugin } from "./RecordingViewPlugin";
import { SortingUnitMetricPlugin } from "./SortingUnitMetricPlugin";
import { SortingUnitViewPlugin } from "./SortingUnitViewPlugin";
import { SortingViewPlugin } from "./SortingViewPlugin";
import { WorkspaceRoute, WorkspaceRouteDispatch } from './WorkspaceRoute';
import { WorkspaceViewPlugin } from "./WorkspaceViewPlugin";
export type { ExternalSortingUnitMetric } from './exteneralUnitMetrics';
export type { Recording, RecordingInfo } from './Recording';
export { recordingSelectionReducer } from './RecordingSelection';
export type { RecordingSelection, RecordingSelectionAction, RecordingSelectionDispatch } from './RecordingSelection';
export type { RecordingViewPlugin, RecordingViewProps } from './RecordingViewPlugin';
export type { Sorting, SortingInfo } from './Sorting';
export { applyMergesToUnit, isMergeGroupRepresentative, mergeGroupForUnitId } from './SortingCuration';
export type { SortingCuration, SortingCurationDispatch } from './SortingCuration';
export { sortingSelectionReducer } from './SortingSelection';
export type { SortingSelection, SortingSelectionAction, SortingSelectionDispatch } from './SortingSelection';
export type { SortingUnitMetricPlugin } from './SortingUnitMetricPlugin';
export type { SortingUnitViewPlugin, SortingUnitViewProps } from './SortingUnitViewPlugin';
export type { SortingViewPlugin, SortingViewProps } from './SortingViewPlugin';
export type { WorkspaceRoute, WorkspaceRouteDispatch } from './WorkspaceRoute';
export declare type MainWindowProps = {
    workspaceUri: string | undefined;
    workspaceRoute: WorkspaceRoute;
    workspaceRouteDispatch: WorkspaceRouteDispatch;
};
export interface MainWindowPlugin extends BaseLabboxPlugin {
    type: 'MainWindow';
    component: FunctionComponent<MainWindowProps>;
}
export interface BaseLabboxPlugin extends BasePlugin {
    priority?: number;
    disabled?: boolean;
    development?: boolean;
}
export interface LabboxViewPlugin extends BaseLabboxPlugin {
    props?: {
        [key: string]: any;
    };
    fullWidth?: boolean;
    defaultExpanded?: boolean;
    singleton?: boolean;
}
export interface LabboxViewProps {
    plugins: LabboxPlugin;
    calculationPool: CalculationPool;
    width?: number;
    height?: number;
}
export declare const filterPlugins: (plugins: LabboxPlugin[]) => LabboxPlugin[];
export declare const sortingViewPlugins: (plugins: LabboxPlugin[]) => SortingViewPlugin[];
export declare const recordingViewPlugins: (plugins: LabboxPlugin[]) => RecordingViewPlugin[];
export declare const sortingUnitViewPlugins: (plugins: LabboxPlugin[]) => SortingUnitViewPlugin[];
export declare const sortingUnitMetricPlugins: (plugins: LabboxPlugin[]) => SortingUnitMetricPlugin[];
export declare type LabboxPlugin = MainWindowPlugin | WorkspaceViewPlugin | SortingViewPlugin | RecordingViewPlugin | SortingUnitViewPlugin | SortingUnitMetricPlugin;
export declare type LabboxExtensionContext = ExtensionContext<LabboxPlugin>;
export declare const useWorkspaceViewPlugins: () => WorkspaceViewPlugin[];
