/// <reference types="react" />
import { RecordingInfo, RecordingSelection, RecordingSelectionDispatch } from "../../pluginInterface";
interface RecordingObject {
}
interface Props {
    recordingObject: RecordingObject;
    recordingInfo: RecordingInfo;
    width: number;
    height: number;
    opts: {
        channelSelectPanel?: boolean;
    };
    recordingSelection?: RecordingSelection;
    recordingSelectionDispatch?: RecordingSelectionDispatch;
}
declare const TimeseriesViewNew: (props: Props) => JSX.Element;
export default TimeseriesViewNew;
