import { FunctionComponent } from 'react';
import { WorkspaceViewProps } from '../../pluginInterface/WorkspaceViewPlugin';
export interface LocationInterface {
    pathname: string;
    search: string;
}
export interface HistoryInterface {
    location: LocationInterface;
    push: (x: LocationInterface) => void;
}
declare const WorkspaceView: FunctionComponent<WorkspaceViewProps>;
export default WorkspaceView;
