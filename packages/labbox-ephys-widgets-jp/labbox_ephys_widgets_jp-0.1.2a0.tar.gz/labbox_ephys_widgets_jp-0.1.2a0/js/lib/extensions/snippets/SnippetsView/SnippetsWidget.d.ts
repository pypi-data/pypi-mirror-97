import { FunctionComponent } from 'react';
import { Recording, Sorting, SortingSelection, SortingSelectionDispatch } from "../../pluginInterface";
declare type Props = {
    recording: Recording;
    sorting: Sorting;
    selection: SortingSelection;
    selectionDispatch: SortingSelectionDispatch;
    unitIds: number[];
    width: number;
    height: number;
};
declare const SnippetsWidget: FunctionComponent<Props>;
export default SnippetsWidget;
