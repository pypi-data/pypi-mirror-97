import { FunctionComponent } from 'react';
import { Recording, Sorting, WorkspaceRoute, WorkspaceRouteDispatch } from "../../pluginInterface";
interface Props {
    recording: Recording;
    sortings: Sorting[];
    workspaceRoute: WorkspaceRoute;
    width: number;
    height: number;
    workspaceRouteDispatch: WorkspaceRouteDispatch;
    onDeleteSortings: (sortingIds: string[]) => void;
}
declare const WorkspaceRecordingView: FunctionComponent<Props>;
export default WorkspaceRecordingView;
