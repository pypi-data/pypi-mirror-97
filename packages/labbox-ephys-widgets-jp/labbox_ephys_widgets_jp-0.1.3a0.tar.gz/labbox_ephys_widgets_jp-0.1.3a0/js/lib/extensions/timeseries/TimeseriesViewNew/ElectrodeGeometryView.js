import React, { useMemo } from 'react';
import ElectrodeGeometryWidget from "../../electrodegeometry/ElectrodeGeometryWidget/ElectrodeGeometryWidget";
const ElectrodeGeometryView = ({ recordingInfo, width, height, selection, visibleElectrodeIds, selectionDispatch }) => {
    const ri = recordingInfo;
    const electrodes = useMemo(() => (ri ? zipElectrodes(ri.geom, ri.channel_ids) : []).filter(a => (visibleElectrodeIds.includes(a.id))), [ri, visibleElectrodeIds]);
    if (!ri) {
        return (React.createElement("div", null, "No recording info found for recording."));
    }
    return (React.createElement(ElectrodeGeometryWidget, { electrodes: electrodes, selection: selection, selectionDispatch: selectionDispatch, width: width, height: height }));
};
const zipElectrodes = (locations, ids) => {
    if (locations && ids && ids.length !== locations.length)
        throw Error('Electrode ID count does not match location count.');
    return ids.map((x, index) => {
        const loc = locations[index];
        return { label: x + '', id: x, x: loc[0], y: loc[1] };
    });
};
export default ElectrodeGeometryView;
//# sourceMappingURL=ElectrodeGeometryView.js.map