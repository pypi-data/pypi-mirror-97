import { FunctionComponent } from 'react';
import { RecordingInfo, RecordingSelection, RecordingSelectionDispatch } from "../../pluginInterface";
interface Props {
    recordingInfo: RecordingInfo;
    width: number;
    height: number;
    selection: RecordingSelection;
    selectionDispatch: RecordingSelectionDispatch;
    visibleElectrodeIds: number[];
}
declare const ElectrodeGeometryView: FunctionComponent<Props>;
export default ElectrodeGeometryView;
