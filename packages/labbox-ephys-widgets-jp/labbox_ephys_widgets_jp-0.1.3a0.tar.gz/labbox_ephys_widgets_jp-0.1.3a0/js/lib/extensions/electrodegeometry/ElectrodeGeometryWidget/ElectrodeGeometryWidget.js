import React, { useMemo } from "react";
import { createElectrodesLayer } from "../../averagewaveforms/AverageWaveformsView/electrodesLayer";
import CanvasWidget from "../../common/CanvasWidget";
import { useLayer, useLayers } from "../../common/CanvasWidget/CanvasWidgetLayer";
const ElectrodeGeometryWidget = (props) => {
    const electrodeLayerProps = useMemo(() => ({
        layoutMode: 'geom',
        electrodeIds: props.electrodes.map(e => e.id),
        electrodeLocations: props.electrodes.map(e => [e.x, e.y]),
        width: props.width,
        height: props.height,
        selection: props.selection,
        selectionDispatch: props.selectionDispatch,
        electrodeOpts: {
            showLabels: true,
            maxElectrodePixelRadius: 25
        },
        noiseLevel: 0,
        samplingFrequency: 0 // not needed
    }), [props]);
    const layer = useLayer(createElectrodesLayer, electrodeLayerProps);
    const layers = useLayers([layer]);
    return (React.createElement(CanvasWidget, Object.assign({ key: 'electrodeGeometryCanvas', layers: layers }, { width: props.width, height: props.height })));
};
export default ElectrodeGeometryWidget;
//# sourceMappingURL=ElectrodeGeometryWidget.js.map