/// <reference types="react" />
import { RecordingSelection, RecordingSelectionDispatch } from "../../pluginInterface";
import { TimeseriesData } from './useTimeseriesModel';
interface Props {
    timeseriesData: TimeseriesData;
    channel_ids: number[];
    channel_locations: (number[])[];
    num_timepoints: number;
    y_scale_factor: number;
    width: number;
    height: number;
    visibleChannelIds?: number[] | null;
    recordingSelection: RecordingSelection;
    recordingSelectionDispatch: RecordingSelectionDispatch;
}
declare const TimeseriesWidgetNew: (props: Props) => JSX.Element;
export default TimeseriesWidgetNew;
