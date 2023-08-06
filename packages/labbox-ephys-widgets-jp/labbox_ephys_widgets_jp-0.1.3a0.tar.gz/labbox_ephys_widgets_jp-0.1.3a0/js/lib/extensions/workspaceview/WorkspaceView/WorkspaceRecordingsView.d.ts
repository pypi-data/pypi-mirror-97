import { FunctionComponent } from 'react';
import { Recording, Sorting, WorkspaceRoute, WorkspaceRouteDispatch } from "../../pluginInterface";
declare type Props = {
    sortings: Sorting[];
    recordings: Recording[];
    workspaceRoute: WorkspaceRoute;
    onDeleteRecordings: (recordingIds: string[]) => void;
    width: number;
    height: number;
    workspaceRouteDispatch: WorkspaceRouteDispatch;
};
declare const WorkspaceRecordingsView: FunctionComponent<Props>;
export default WorkspaceRecordingsView;
