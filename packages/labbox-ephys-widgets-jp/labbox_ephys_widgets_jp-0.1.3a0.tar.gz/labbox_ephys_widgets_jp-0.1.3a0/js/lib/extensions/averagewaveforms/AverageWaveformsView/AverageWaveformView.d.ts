import { FunctionComponent } from 'react';
import { ActionItem, DividerItem } from '../../common/Toolbars';
import { Recording, Sorting, SortingSelection, SortingSelectionDispatch } from "../../pluginInterface";
declare type Props = {
    sorting: Sorting;
    recording: Recording;
    unitId: number;
    selection: SortingSelection;
    selectionDispatch: SortingSelectionDispatch;
    width: number;
    height: number;
    noiseLevel: number;
    customActions?: (ActionItem | DividerItem)[];
};
declare const AverageWaveformView: FunctionComponent<Props>;
export default AverageWaveformView;
