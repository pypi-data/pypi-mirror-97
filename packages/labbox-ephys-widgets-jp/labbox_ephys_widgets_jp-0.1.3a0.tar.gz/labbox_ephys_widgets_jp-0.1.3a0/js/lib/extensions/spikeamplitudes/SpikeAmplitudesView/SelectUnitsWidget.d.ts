import { FunctionComponent } from 'react';
import { Sorting, SortingSelection, SortingSelectionDispatch } from "../../pluginInterface";
declare type Props = {
    sorting: Sorting;
    selection: SortingSelection;
    selectionDispatch: SortingSelectionDispatch;
};
declare const SelectUnitsWidget: FunctionComponent<Props>;
export default SelectUnitsWidget;
