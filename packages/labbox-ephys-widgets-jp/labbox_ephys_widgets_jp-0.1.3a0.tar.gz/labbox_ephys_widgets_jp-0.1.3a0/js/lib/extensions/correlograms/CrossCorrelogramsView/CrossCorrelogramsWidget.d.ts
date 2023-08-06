import { FunctionComponent } from 'react';
import { Sorting, SortingSelection, SortingSelectionDispatch } from "../../pluginInterface";
declare type Props = {
    sorting: Sorting;
    selection: SortingSelection;
    selectionDispatch: SortingSelectionDispatch;
    unitIds: number[];
    width: number;
    height: number;
};
declare const CrossCorrelogramsWidget: FunctionComponent<Props>;
export default CrossCorrelogramsWidget;
