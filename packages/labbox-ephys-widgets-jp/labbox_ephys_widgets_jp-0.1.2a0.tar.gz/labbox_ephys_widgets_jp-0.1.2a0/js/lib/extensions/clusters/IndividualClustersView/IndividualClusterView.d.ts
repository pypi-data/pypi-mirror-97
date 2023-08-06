import { FunctionComponent } from 'react';
import { Recording, Sorting, SortingSelection, SortingSelectionDispatch } from "../../pluginInterface";
declare type Props = {
    recording: Recording;
    sorting: Sorting;
    selection: SortingSelection;
    selectionDispatch: SortingSelectionDispatch;
    unitId: number;
    width: number;
    height: number;
};
declare const IndividualClusterView: FunctionComponent<Props>;
export default IndividualClusterView;
