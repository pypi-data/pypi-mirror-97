import React, { useMemo, useReducer } from 'react';
import Splitter from '../../common/Splitter';
import { recordingSelectionReducer } from "../../pluginInterface";
import ElectrodeGeometryView from './ElectrodeGeometryView';
import TimeseriesWidgetNew from './TimeseriesWidgetNew';
import useTimeseriesData from './useTimeseriesModel';
// interface TimeseriesInfo {
//     samplerate: number
//     segment_size: number
//     num_channels: number
//     channel_ids: number[]
//     channel_locations: (number[])[]
//     num_timepoints: number
//     y_offsets: number[]
//     y_scale_factor: number
//     initial_y_scale_factor: number
// }
const TimeseriesViewNew = (props) => {
    const opts = props.opts;
    const recordingInfo = props.recordingInfo;
    const timeseriesData = useTimeseriesData(props.recordingObject, props.recordingInfo);
    const [recordingSelectionInternal, recordingSelectionInternalDispatch] = useReducer(recordingSelectionReducer, {});
    const recordingSelection = props.recordingSelection || recordingSelectionInternal;
    const recordingSelectionDispatch = props.recordingSelectionDispatch || recordingSelectionInternalDispatch;
    const selectedElectrodeIds = useMemo(() => (recordingSelection.selectedElectrodeIds || []), [recordingSelection.selectedElectrodeIds]);
    const visibleElectrodeIds = useMemo(() => (recordingSelection.visibleElectrodeIds || recordingInfo.channel_ids), [recordingSelection.visibleElectrodeIds, recordingInfo.channel_ids]);
    const y_scale_factor = 1 / (props.recordingInfo.noise_level || 1) * 1 / 10;
    if (timeseriesData) {
        return (React.createElement("div", null,
            React.createElement(Splitter, { width: props.width, height: props.height, initialPosition: 200 },
                opts.channelSelectPanel && (React.createElement(ElectrodeGeometryView, { recordingInfo: props.recordingInfo, width: 0, height: 0, visibleElectrodeIds: visibleElectrodeIds, selection: recordingSelection, selectionDispatch: recordingSelectionDispatch })),
                ((!opts.channelSelectPanel) || (selectedElectrodeIds.length > 0) || (visibleElectrodeIds.length <= 12)) ? (React.createElement(TimeseriesWidgetNew, { timeseriesData: timeseriesData, channel_ids: props.recordingInfo.channel_ids, channel_locations: props.recordingInfo.geom, num_timepoints: props.recordingInfo.num_frames, 
                    // y_offsets={timeseriesInfo.y_offsets}
                    // y_scale_factor={timeseriesInfo.y_scale_factor * (timeseriesInfo.initial_y_scale_factor || 1)}
                    y_scale_factor: y_scale_factor, width: props.width, height: props.height, visibleChannelIds: opts.channelSelectPanel ? (selectedElectrodeIds.length > 0 ? selectedElectrodeIds : visibleElectrodeIds) : null, recordingSelection: recordingSelection, recordingSelectionDispatch: recordingSelectionDispatch })) : (React.createElement("div", null, "Select one or more electrodes")))));
    }
    else {
        return (React.createElement("div", null, "Creating timeseries model"));
    }
};
// const calculateTimeseriesInfo = async (recordingObject: RecordingObject, hither: HitherInterface): Promise<TimeseriesInfo> => {
//     let info: TimeseriesInfo
//     try {
//         info = await hither.createHitherJob(
//             'createjob_calculate_timeseries_info',
//             { recording_object: recordingObject },
//             {
//                 useClientCache: true
//             }
//         ).wait() as TimeseriesInfo
//     }
//     catch (err) {
//         console.error(err);
//         throw Error('Problem calculating timeseries info.')
//     }
//     if (!info) {
//         throw Error('Unexpected problem calculating timeseries info: info is null.')
//     }
//     return info
// }
export default TimeseriesViewNew;
//# sourceMappingURL=TimeseriesViewNew.js.map