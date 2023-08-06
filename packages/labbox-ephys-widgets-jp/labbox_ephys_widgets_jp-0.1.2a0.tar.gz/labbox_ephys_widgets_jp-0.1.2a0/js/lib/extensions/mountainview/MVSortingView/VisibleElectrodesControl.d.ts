import { FunctionComponent } from 'react';
import { RecordingInfo, SortingSelection, SortingSelectionDispatch } from "../../pluginInterface";
declare type Props = {
    recordingInfo: RecordingInfo;
    selection: SortingSelection;
    selectionDispatch: SortingSelectionDispatch;
};
declare const VisibleElectrodesControl: FunctionComponent<Props>;
export default VisibleElectrodesControl;
