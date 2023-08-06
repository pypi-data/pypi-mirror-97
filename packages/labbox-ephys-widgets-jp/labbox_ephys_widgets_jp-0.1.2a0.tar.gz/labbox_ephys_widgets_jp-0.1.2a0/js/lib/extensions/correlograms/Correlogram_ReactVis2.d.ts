import { FunctionComponent } from 'react';
import { Sorting, SortingSelection, SortingSelectionDispatch } from "../pluginInterface";
declare type Props = {
    sorting: Sorting;
    unitId1: number;
    unitId2?: number;
    selection: SortingSelection;
    selectionDispatch: SortingSelectionDispatch;
    width: number;
    height: number;
};
declare const Correlogram_rv2: FunctionComponent<Props>;
export default Correlogram_rv2;
