import { ServerInfo } from 'labbox/lib/LabboxProvider';
declare type Page = 'recordings' | 'recording' | 'sorting';
export declare const isWorkspacePage: (x: string) => x is Page;
declare type WorkspaceRecordingsRoute = {
    page: 'recordings';
    workspaceUri?: string;
};
declare type WorspaceRecordingRoute = {
    page: 'recording';
    recordingId: string;
    workspaceUri?: string;
};
declare type WorspaceSortingRoute = {
    page: 'sorting';
    recordingId: string;
    sortingId: string;
    workspaceUri?: string;
};
export declare type WorkspaceRoute = WorkspaceRecordingsRoute | WorspaceRecordingRoute | WorspaceSortingRoute;
declare type GotoRecordingsPageAction = {
    type: 'gotoRecordingsPage';
};
declare type GotoRecordingPageAction = {
    type: 'gotoRecordingPage';
    recordingId: string;
};
declare type GotoSortingPageAction = {
    type: 'gotoSortingPage';
    recordingId: string;
    sortingId: string;
};
export declare type WorkspaceRouteAction = GotoRecordingsPageAction | GotoRecordingPageAction | GotoSortingPageAction;
export declare type WorkspaceRouteDispatch = (a: WorkspaceRouteAction) => void;
export interface LocationInterface {
    pathname: string;
    search: string;
}
export interface HistoryInterface {
    location: LocationInterface;
    push: (x: LocationInterface) => void;
}
export declare const routeFromLocation: (location: LocationInterface, serverInfo: ServerInfo | null) => WorkspaceRoute;
export declare const locationFromRoute: (route: WorkspaceRoute) => {
    pathname: string;
    search: string;
};
export declare const workspaceRouteReducer: (s: WorkspaceRoute, a: WorkspaceRouteAction) => WorkspaceRoute;
export {};
