import { Recording } from "./Recording";
import { Sorting } from "./Sorting";
import { SortingCuration } from "./SortingCuration";
export declare type WorkspaceState = {
    recordings: Recording[];
    sortings: Sorting[];
};
declare type AddRecordingWorkspaceAction = {
    type: 'ADD_RECORDING';
    recording: Recording;
};
declare type DeleteRecordingsWorkspaceAction = {
    type: 'DELETE_RECORDINGS';
    recordingIds: string[];
};
declare type AddSortingsWorkspaceAction = {
    type: 'ADD_SORTING';
    sorting: Sorting;
};
declare type DeleteSortingsWorkspaceAction = {
    type: 'DELETE_SORTINGS';
    sortingIds: string[];
};
declare type DeleteSortingsForRecordingsWorkspaceAction = {
    type: 'DELETE_SORTINGS_FOR_RECORDINGS';
    recordingIds: string[];
};
export interface AddUnitLabelWorkspaceAction {
    type: 'ADD_UNIT_LABEL';
    sortingId: string;
    unitId: number;
    label: string;
}
export interface RemoveUnitLabelWorkspaceAction {
    type: 'REMOVE_UNIT_LABEL';
    sortingId: string;
    unitId: number;
    label: string;
}
export interface MergeUnitsAction {
    type: 'MERGE_UNITS';
    sortingId: string;
    unitIds: number[];
}
export interface UnmergeUnitsAction {
    type: 'UNMERGE_UNITS';
    sortingId: string;
    unitIds: number[];
}
export interface SetSortingCurationWorkspaceAction {
    type: 'SET_CURATION';
    curation: SortingCuration;
}
export declare type SortingCurationWorkspaceAction = AddUnitLabelWorkspaceAction | RemoveUnitLabelWorkspaceAction | SetSortingCurationWorkspaceAction | MergeUnitsAction | UnmergeUnitsAction;
export declare type WorkspaceAction = AddRecordingWorkspaceAction | DeleteRecordingsWorkspaceAction | AddSortingsWorkspaceAction | DeleteSortingsWorkspaceAction | DeleteSortingsForRecordingsWorkspaceAction | SortingCurationWorkspaceAction;
export declare const sortingCurationReducer: (state: SortingCuration, action: SortingCurationWorkspaceAction) => SortingCuration;
declare const workspaceReducer: (s: WorkspaceState, a: WorkspaceAction) => WorkspaceState;
export declare type WorkspaceDispatch = (a: WorkspaceAction) => void;
export default workspaceReducer;
