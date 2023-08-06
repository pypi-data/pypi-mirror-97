import { FunctionComponent } from 'react';
import { HistoryInterface, LocationInterface, WorkspaceRoute, WorkspaceRouteDispatch } from './extensions/pluginInterface/WorkspaceRoute';
interface Props {
    workspaceUri: string;
}
export declare const useWorkspaceRoute: (location: LocationInterface, history: HistoryInterface, workspaceUri: string | undefined) => [WorkspaceRoute, WorkspaceRouteDispatch];
declare const WorkspaceViewWrapper: FunctionComponent<Props>;
export default WorkspaceViewWrapper;
