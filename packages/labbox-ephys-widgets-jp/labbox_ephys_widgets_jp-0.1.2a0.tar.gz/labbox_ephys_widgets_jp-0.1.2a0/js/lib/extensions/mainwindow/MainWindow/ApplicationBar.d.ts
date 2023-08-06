import { FunctionComponent } from 'react';
import { WorkspaceRouteDispatch } from '../../pluginInterface';
declare type Props = {
    onOpenSettings: () => void;
    workspaceRouteDispatch: WorkspaceRouteDispatch;
    logo?: any;
};
declare const ApplicationBar: FunctionComponent<Props>;
export default ApplicationBar;
