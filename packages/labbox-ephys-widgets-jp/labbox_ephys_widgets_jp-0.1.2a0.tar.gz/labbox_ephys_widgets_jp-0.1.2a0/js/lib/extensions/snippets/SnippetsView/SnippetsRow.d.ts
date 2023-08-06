import { FunctionComponent } from 'react';
import { Recording, Sorting, SortingSelection, SortingSelectionDispatch } from "../../pluginInterface";
declare type Props = {
    recording: Recording;
    sorting: Sorting;
    noiseLevel: number;
    selection: SortingSelection;
    selectionDispatch: SortingSelectionDispatch;
    unitId: number;
    height: number;
};
export declare type Snippet = {
    timepoint: number;
    index: number;
    unitId: number;
    waveform?: number[][];
};
declare const SnippetsRow: FunctionComponent<Props>;
export default SnippetsRow;
