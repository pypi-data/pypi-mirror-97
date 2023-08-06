import { Reducer } from "react";
import { RecordingSelection, RecordingSelectionAction } from "./RecordingSelection";
import { SortingCuration } from "./SortingCuration";
export interface SortingSelection extends RecordingSelection {
    selectedUnitIds?: number[];
    visibleUnitIds?: number[] | null;
    applyMerges?: boolean;
}
export declare type SortingSelectionDispatch = (action: SortingSelectionAction) => void;
declare type SetSelectionSortingSelectionAction = {
    type: 'SetSelection';
    selection: SortingSelection;
};
declare type SetSelectedUnitIdsSortingSelectionAction = {
    type: 'SetSelectedUnitIds';
    selectedUnitIds: number[];
};
declare type SetVisibleUnitIdsSortingSelectionAction = {
    type: 'SetVisibleUnitIds';
    visibleUnitIds: number[] | null;
};
declare type SetSortingSelectionAction = {
    type: 'Set';
    state: SortingSelection;
};
declare type UnitClickedSortingSelectionAction = {
    type: 'UnitClicked';
    unitId: number;
    ctrlKey?: boolean;
    shiftKey?: boolean;
};
declare type ToggleApplyMergesSortingSelectionAction = {
    type: 'ToggleApplyMerges';
    curation?: SortingCuration;
};
export declare type SortingSelectionAction = SetSelectionSortingSelectionAction | SetSelectedUnitIdsSortingSelectionAction | SetVisibleUnitIdsSortingSelectionAction | UnitClickedSortingSelectionAction | SetSortingSelectionAction | ToggleApplyMergesSortingSelectionAction | RecordingSelectionAction;
export declare const sortingSelectionReducer: Reducer<SortingSelection, SortingSelectionAction>;
export {};
