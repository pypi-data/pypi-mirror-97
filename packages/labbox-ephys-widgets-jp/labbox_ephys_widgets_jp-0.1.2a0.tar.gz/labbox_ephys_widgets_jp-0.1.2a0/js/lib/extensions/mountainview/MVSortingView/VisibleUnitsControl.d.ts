import { FunctionComponent } from 'react';
import { Recording, Sorting, SortingSelection, SortingSelectionDispatch } from "../../pluginInterface";
declare type Props = {
    sorting: Sorting;
    recording: Recording;
    selection: SortingSelection;
    selectionDispatch: SortingSelectionDispatch;
};
declare const VisibleUnitsControl: FunctionComponent<Props>;
export default VisibleUnitsControl;
