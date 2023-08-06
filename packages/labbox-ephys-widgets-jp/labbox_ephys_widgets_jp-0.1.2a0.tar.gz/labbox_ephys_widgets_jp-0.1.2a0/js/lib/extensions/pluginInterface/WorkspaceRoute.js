import QueryString from 'querystring';
export const isWorkspacePage = (x) => {
    return ['recordings', 'recording', 'sorting'].includes(x);
};
export const routeFromLocation = (location, serverInfo) => {
    const pathList = location.pathname.split('/');
    const query = QueryString.parse(location.search.slice(1));
    const workspace = query.workspace || 'default';
    const defaultFeedId = serverInfo === null || serverInfo === void 0 ? void 0 : serverInfo.defaultFeedId;
    const workspaceUri = workspace.startsWith('workspace://') ? workspace : (defaultFeedId ? `workspace://${defaultFeedId}/${workspace}` : undefined);
    const page = pathList[1] || 'recordings';
    if (!isWorkspacePage(page))
        throw Error(`Invalid page: ${page}`);
    switch (page) {
        case 'recordings': return {
            workspaceUri,
            page
        };
        case 'recording': return {
            workspaceUri,
            page,
            recordingId: pathList[2]
        };
        case 'sorting': return {
            workspaceUri,
            page,
            recordingId: pathList[2] || '',
            sortingId: pathList[3] || ''
        };
        default: return {
            workspaceUri,
            page: 'recordings'
        };
    }
};
export const locationFromRoute = (route) => {
    const queryParams = {};
    if (route.workspaceUri) {
        queryParams['workspace'] = route.workspaceUri;
    }
    switch (route.page) {
        case 'recordings': return {
            pathname: `/`,
            search: queryString(queryParams)
        };
        case 'recording': return {
            pathname: `/recording/${route.recordingId}`,
            search: queryString(queryParams)
        };
        case 'sorting': return {
            pathname: `/sorting/${route.recordingId}/${route.sortingId}`,
            search: queryString(queryParams)
        };
    }
};
var queryString = (params) => {
    const keys = Object.keys(params);
    if (keys.length === 0)
        return '';
    return '?' + (keys.map((key) => {
        return encodeURIComponent(key) + '=' + encodeURIComponent(params[key]);
    }).join('&'));
};
export const workspaceRouteReducer = (s, a) => {
    let newRoute = s;
    switch (a.type) {
        case 'gotoRecordingsPage':
            newRoute = {
                page: 'recordings',
                workspaceUri: s.workspaceUri
            };
            break;
        case 'gotoRecordingPage':
            newRoute = {
                page: 'recording',
                recordingId: a.recordingId,
                workspaceUri: s.workspaceUri
            };
            break;
        case 'gotoSortingPage':
            newRoute = {
                page: 'sorting',
                recordingId: a.recordingId,
                sortingId: a.sortingId,
                workspaceUri: s.workspaceUri
            };
            break;
    }
    return newRoute;
};
//# sourceMappingURL=WorkspaceRoute.js.map