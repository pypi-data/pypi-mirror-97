import React from 'react';
import { ExternalSortingUnitMetric, Recording, Sorting, WorkspaceRouteDispatch } from '../../pluginInterface';
import { SortingCurationWorkspaceAction } from '../../pluginInterface/workspaceReducer';
interface Props {
    sorting: Sorting;
    recording: Recording;
    width: number;
    height: number;
    workspaceRouteDispatch: WorkspaceRouteDispatch;
    readOnly: boolean;
    onSetExternalUnitMetrics: (a: {
        sortingId: string;
        externalUnitMetrics: ExternalSortingUnitMetric[];
    }) => void;
    curationDispatch: (a: SortingCurationWorkspaceAction) => void;
}
declare const SortingView: React.FunctionComponent<Props>;
export default SortingView;
