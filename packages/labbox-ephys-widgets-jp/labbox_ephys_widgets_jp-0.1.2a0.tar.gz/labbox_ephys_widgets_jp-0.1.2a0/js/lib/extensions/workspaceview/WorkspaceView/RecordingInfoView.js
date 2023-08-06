// convert to tsx
import { Table, TableBody, TableCell, TableHead, TableRow } from '@material-ui/core';
import React, { useMemo, useReducer } from 'react';
import ElectrodeGeometryWidget from '../../electrodegeometry/ElectrodeGeometryWidget/ElectrodeGeometryWidget';
import { recordingSelectionReducer } from "../../pluginInterface";
const zipElectrodes = (locations, ids) => {
    if (locations && ids && ids.length !== locations.length)
        throw Error('Electrode ID count does not match location count.');
    return ids.map((x, index) => {
        const loc = locations[index];
        return { label: x + '', x: loc[0], y: loc[1], id: x };
    });
};
const RecordingInfoView = ({ recordingInfo, hideElectrodeGeometry }) => {
    const ri = recordingInfo;
    const electrodes = useMemo(() => (ri ? zipElectrodes(ri.geom, ri.channel_ids) : []), [ri]);
    const [selection, selectionDispatch] = useReducer(recordingSelectionReducer, {});
    if (!ri) {
        return (React.createElement("div", null, "No recording info found for recording."));
    }
    return (React.createElement(React.Fragment, null,
        React.createElement("div", { style: { width: 600 } },
            React.createElement(RecordingViewTable, { sampling_frequency: ri.sampling_frequency, num_frames: ri.num_frames, channel_ids: ri.channel_ids, channel_groups: ri.channel_groups, noise_level: ri.noise_level })),
        !hideElectrodeGeometry && (React.createElement(ElectrodeGeometryWidget, { electrodes: electrodes, selection: selection, selectionDispatch: selectionDispatch, width: 350, height: 150 }))));
};
const RecordingViewTable = ({ sampling_frequency, channel_ids, channel_groups, num_frames, noise_level }) => {
    return (React.createElement(Table, { className: "NiceTable" },
        React.createElement(TableHead, null),
        React.createElement(TableBody, null,
            React.createElement(TableRow, null,
                React.createElement(TableCell, null, "Sampling frequency"),
                React.createElement(TableCell, null, sampling_frequency)),
            React.createElement(TableRow, null,
                React.createElement(TableCell, null, "Num. frames"),
                React.createElement(TableCell, null, num_frames)),
            React.createElement(TableRow, null,
                React.createElement(TableCell, null, "Duration (min)"),
                React.createElement(TableCell, null, num_frames / sampling_frequency / 60)),
            React.createElement(TableRow, null,
                React.createElement(TableCell, null, "Num. channels"),
                React.createElement(TableCell, null, channel_ids.length)),
            React.createElement(TableRow, null,
                React.createElement(TableCell, null, "Channel IDs"),
                React.createElement(TableCell, null, channel_ids.length < 20 ? commasep(channel_ids) : commasep(channel_ids.slice(0, 20)) + ' ...')),
            React.createElement(TableRow, null,
                React.createElement(TableCell, null, "Channel groups"),
                React.createElement(TableCell, null, channel_groups.length < 20 ? commasep(channel_groups) : commasep(channel_groups.slice(0, 20)) + ' ...')),
            React.createElement(TableRow, null,
                React.createElement(TableCell, null, "Noise level"),
                React.createElement(TableCell, null, noise_level)))));
};
function commasep(x) {
    return x.map(a => (a + '')).join(', ');
}
export default RecordingInfoView;
//# sourceMappingURL=RecordingInfoView.js.map