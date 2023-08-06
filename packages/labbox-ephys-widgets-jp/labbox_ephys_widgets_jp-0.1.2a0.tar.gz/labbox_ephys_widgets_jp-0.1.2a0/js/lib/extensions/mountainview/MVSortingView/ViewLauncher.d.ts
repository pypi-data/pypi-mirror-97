import { FunctionComponent } from 'react';
import { SortingSelection, SortingUnitViewPlugin, SortingViewPlugin } from "../../pluginInterface";
export declare type ViewPluginType = 'RecordingView' | 'SortingView' | 'SortingUnitView';
declare type Props = {
    selection: SortingSelection;
    onLaunchSortingView: (plugin: SortingViewPlugin) => void;
    onLaunchSortingUnitView: (plugin: SortingUnitViewPlugin, unitId: number, label: string) => void;
};
declare const ViewLauncher: FunctionComponent<Props>;
export default ViewLauncher;
