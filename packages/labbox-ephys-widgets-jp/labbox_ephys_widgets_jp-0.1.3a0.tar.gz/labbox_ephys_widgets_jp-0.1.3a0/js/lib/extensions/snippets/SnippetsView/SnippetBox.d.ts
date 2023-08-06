import { FunctionComponent } from 'react';
import { SortingSelection, SortingSelectionDispatch } from "../../pluginInterface";
import { Snippet } from './SnippetsRow';
declare type Props = {
    snippet: Snippet | null;
    noiseLevel: number;
    samplingFrequency: number;
    electrodeIds: number[];
    electrodeLocations: number[][];
    selection: SortingSelection;
    selectionDispatch: SortingSelectionDispatch;
    width: number;
    height: number;
};
declare const SnippetBox: FunctionComponent<Props>;
export default SnippetBox;
