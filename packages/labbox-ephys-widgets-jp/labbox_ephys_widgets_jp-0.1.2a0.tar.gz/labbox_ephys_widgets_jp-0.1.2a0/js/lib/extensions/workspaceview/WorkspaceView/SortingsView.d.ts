import { FunctionComponent } from 'react';
import { Sorting, WorkspaceRoute, WorkspaceRouteDispatch } from "../../pluginInterface";
declare type Props = {
    sortings: Sorting[];
    workspaceRouteDispatch: WorkspaceRouteDispatch;
    workspaceRoute: WorkspaceRoute;
    onDeleteSortings: (sortingIds: string[]) => void;
};
declare const SortingsView: FunctionComponent<Props>;
export default SortingsView;
