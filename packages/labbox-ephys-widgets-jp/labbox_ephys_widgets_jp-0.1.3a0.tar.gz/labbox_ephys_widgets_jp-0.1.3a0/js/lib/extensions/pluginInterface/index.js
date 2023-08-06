import { usePlugins } from "labbox";
import { useMemo } from "react";
export { recordingSelectionReducer } from './RecordingSelection';
export { applyMergesToUnit, isMergeGroupRepresentative, mergeGroupForUnitId } from './SortingCuration';
export { sortingSelectionReducer } from './SortingSelection';
export const filterPlugins = (plugins) => {
    return plugins.filter(p => ((!p.disabled) && (!p.development)));
};
export const sortingViewPlugins = (plugins) => {
    return filterPlugins(plugins).filter(p => (p.type === 'SortingView'))
        .map(p => p);
};
export const recordingViewPlugins = (plugins) => {
    return filterPlugins(plugins).filter(p => (p.type === 'RecordingView'))
        .map(p => p);
};
export const sortingUnitViewPlugins = (plugins) => {
    return filterPlugins(plugins).filter(p => (p.type === 'SortingUnitView'))
        .map(p => p);
};
export const sortingUnitMetricPlugins = (plugins) => {
    return filterPlugins(plugins).filter(p => (p.type === 'SortingUnitMetric'))
        .map(p => p);
};
export const useWorkspaceViewPlugins = () => {
    const plugins = usePlugins();
    return useMemo(() => (plugins.filter(p => (p.type === 'WorkspaceView')).map(p => p)), [plugins]);
};
//# sourceMappingURL=index.js.map