import WorkspaceView from "./WorkspaceView";
export function activate(context) {
    context.registerPlugin({
        type: 'WorkspaceView',
        name: 'WorkspaceView',
        label: 'Workspace View',
        component: WorkspaceView
    });
}
//# sourceMappingURL=workspaceview.js.map