import React, { useEffect, useMemo, useReducer, useState } from 'react';
import CanvasWidget from "../../common/CanvasWidget";
import { useLayer, useLayers } from "../../common/CanvasWidget/CanvasWidgetLayer";
import { useRecordingInfo } from '../../common/useRecordingInfo';
import { createElectrodeGeometryLayer } from "../../electrodegeometry/ElectrodeGeometryWidget/electrodeGeometryLayer";
const updateIndexReducer = (state, action) => {
    return state + 1;
};
// this is duplicate code
const zipElectrodes = (locations, ids) => {
    if (locations && ids && ids.length !== locations.length)
        throw Error('Electrode ID count does not match location count.');
    return ids.map((x, index) => {
        const loc = locations[index];
        return { label: x + '', x: loc[0], y: loc[1], electrodeId: x };
    });
};
const valToColor = (v) => {
    if (v <= 0)
        return 'black';
    if (v >= 1)
        return 'white';
    const x = Math.floor(v * 255);
    return `rgb(${x}, ${x}, ${x})`;
};
const FireTrackWidget = ({ recording, timeseriesData, selection, width, height }) => {
    const selectedElectrodeIds = selection.selectedElectrodeIds;
    const [data, setData] = useState({});
    const [updateIndex, updateIndexDispatch] = useReducer(updateIndexReducer, 0);
    useEffect(() => {
        const t = selection.currentTimepoint;
        if ((t === undefined) || (!selectedElectrodeIds) || (!timeseriesData)) {
            setData({});
            return;
        }
        const d = {};
        for (let eid of selectedElectrodeIds) {
            const x = timeseriesData.getChannelData(eid, Math.floor(t), Math.floor(t) + 1, 1);
            d[eid + ''] = x[0];
        }
        setData(d);
        const somethingMissing = (Object.values(d).filter(v => isNaN(v)).length > 0);
        if (somethingMissing) {
            setTimeout(() => {
                updateIndexDispatch({ type: 'increment' });
            }, 500);
        }
    }, [timeseriesData, selection, selectedElectrodeIds, setData, updateIndex, updateIndexDispatch]);
    const ri = useRecordingInfo(recording.recordingObject);
    const electrodes = useMemo(() => {
        const scaleFactor = (selection.ampScaleFactor || 1) / ((ri === null || ri === void 0 ? void 0 : ri.noise_level) || 1) * 1 / 5;
        const colorForElectrode = (id) => {
            const val = data[id];
            if (isNaN(val))
                return 'lightgray';
            const adjustedVal = -val * scaleFactor;
            return valToColor(adjustedVal);
        };
        return (ri ? zipElectrodes(ri.geom, ri.channel_ids) : []).map(e => (Object.assign(Object.assign({}, e), { id: e.electrodeId, color: colorForElectrode(e.electrodeId) })));
    }, [ri, data, selection.ampScaleFactor]);
    const layerProps = {
        electrodes,
        selectedElectrodeIds: useMemo(() => (selection.selectedElectrodeIds || []), [selection.selectedElectrodeIds]),
        onSelectedElectrodeIdsChanged: useMemo(() => ((x) => { }), []),
        width,
        height
    };
    const layer = useLayer(createElectrodeGeometryLayer, layerProps);
    const layers = useLayers([layer]);
    return (React.createElement(CanvasWidget, Object.assign({ layers: layers }, { width, height })));
};
export default FireTrackWidget;
//# sourceMappingURL=FireTrackWidget.js.map