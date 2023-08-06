import { FunctionComponent } from 'react';
import { Sorting, WorkspaceRouteDispatch } from "../../pluginInterface";
interface Props {
    sortings: Sorting[];
    workspaceRouteDispatch: WorkspaceRouteDispatch;
    readOnly: boolean;
    onDeleteSortings: (sortingIds: string[]) => void;
}
declare const SortingsTable: FunctionComponent<Props>;
export default SortingsTable;
