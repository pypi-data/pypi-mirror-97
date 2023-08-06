import React, { useCallback } from 'react';
import SortingView from './SortingView';
import WorkspaceRecordingsView from './WorkspaceRecordingsView';
import WorkspaceRecordingView from './WorkspaceRecordingView';
// export const useWorkspaceRoute = (location: LocationInterface, history: HistoryInterface, workspaceInfo: WorkspaceInfo | undefined): [WorkspaceRoute, WorkspaceRouteDispatch] => {
//   const workspaceRouteDispatch = useMemo(() => ((a: WorkspaceRouteAction) => {
//     const route = routeFromLocation(history.location)
//     let newRoute: WorkspaceRoute | null = null
//     switch (a.type) {
//       case 'gotoRecordingsPage': newRoute = {
//         page: 'recordings',
//         workspaceName: route.workspaceName
//       }; break;
//       case 'gotoRecordingPage': newRoute = {
//         page: 'recording',
//         recordingId: a.recordingId,
//         workspaceName: route.workspaceName
//       }; break;
//       case 'gotoSortingPage': newRoute = {
//         page: 'sorting',
//         recordingId: a.recordingId,
//         sortingId: a.sortingId,
//         workspaceName: route.workspaceName
//       }; break
//     }
//     if (newRoute) {
//       history.push(locationFromRoute(newRoute, workspaceInfo || { workspaceName: '', feedUri: '', readOnly: true }))
//     }
//   }), [history, workspaceInfo])
//   const workspaceRoute = useMemo(() => {
//     return routeFromLocation(location)
//   }, [location])
//   return [workspaceRoute, workspaceRouteDispatch]
// }
const WorkspaceView = ({ workspace, workspaceDispatch, workspaceRoute, workspaceRouteDispatch, width = 500, height = 500 }) => {
    const handleDeleteRecordings = useCallback((recordingIds) => {
        workspaceDispatch({
            type: 'DELETE_RECORDINGS',
            recordingIds
        });
    }, [workspaceDispatch]);
    const handleDeleteSortings = useCallback((sortingIds) => {
        workspaceDispatch({
            type: 'DELETE_SORTINGS',
            sortingIds
        });
    }, [workspaceDispatch]);
    const curationDispatch = useCallback((a) => {
        workspaceDispatch(a);
    }, [workspaceDispatch]);
    switch (workspaceRoute.page) {
        case 'recordings': return (React.createElement(WorkspaceRecordingsView, Object.assign({ onDeleteRecordings: handleDeleteRecordings }, { width, height, recordings: workspace.recordings, sortings: workspace.sortings, workspaceRoute, workspaceRouteDispatch })));
        case 'recording': {
            const rid = workspaceRoute.recordingId;
            const recording = workspace.recordings.filter(r => (r.recordingId === rid))[0];
            if (!recording)
                return React.createElement("div", null,
                    "Recording not found: ",
                    rid);
            return (React.createElement(WorkspaceRecordingView, Object.assign({ onDeleteSortings: handleDeleteSortings }, { width, height, recording, workspaceRouteDispatch, workspaceRoute }, { sortings: workspace.sortings.filter(s => (s.recordingId === rid)) })));
        }
        case 'sorting': {
            const rid = workspaceRoute.recordingId;
            const recording = workspace.recordings.filter(r => (r.recordingId === rid))[0];
            if (!recording)
                return React.createElement("div", null,
                    "Recording not found: ",
                    rid);
            const sid = workspaceRoute.sortingId;
            const sorting = workspace.sortings.filter(s => (s.recordingId === rid && s.sortingId === sid))[0];
            if (!sorting)
                return React.createElement("div", null,
                    "Sorting not found: ",
                    rid,
                    "/",
                    sid);
            return (React.createElement(SortingView, { sorting: sorting, recording: recording, onSetExternalUnitMetrics: (a) => { }, curationDispatch: curationDispatch, width: width, height: height, readOnly: false, workspaceRouteDispatch: workspaceRouteDispatch }));
        }
    }
};
export default WorkspaceView;
//# sourceMappingURL=WorkspaceView.js.map