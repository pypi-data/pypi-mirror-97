import { rectangularRegionsIntersect } from '../../common/CanvasWidget/Geometry';
import { setCanvasFromProps } from './ElectrodeGeometry';
// This could just as well have gone in the ElectrodeGeometry.tsx file since it touches on the data that's 'owned' by the
// ElectrodeGeometry component; however, the functions in this file are the only things consuming it right now.
// A different implementation might do things differently.
const getElectrodeBoundingRect = (e, r, fill = false) => {
    const myRadius = fill ? r - 1 : r;
    return {
        xmin: e.x - myRadius,
        ymin: e.y - myRadius,
        xmax: e.x + myRadius,
        ymax: e.y + myRadius
    };
};
export const setDragLayerStateFromProps = (layer, layerProps) => {
    var _a, _b, _c;
    setCanvasFromProps(layer, layerProps);
    let layerState = layer.getState();
    layerState = Object.assign(Object.assign({}, layerState), { electrodeBoundingBoxes: (_a = layerState === null || layerState === void 0 ? void 0 : layerState.electrodeBoundingBoxes) !== null && _a !== void 0 ? _a : [], selectedElectrodes: (_b = layerState === null || layerState === void 0 ? void 0 : layerState.selectedElectrodes) !== null && _b !== void 0 ? _b : [], draggedElectrodes: (_c = layerState === null || layerState === void 0 ? void 0 : layerState.draggedElectrodes) !== null && _c !== void 0 ? _c : [] });
    const { electrodes, electrodeRadius } = layerProps;
    const rects = electrodes.map((e) => { return Object.assign(Object.assign({}, e), { br: getElectrodeBoundingRect(e, electrodeRadius) }); });
    layer.setState(Object.assign(Object.assign({}, layerState), { electrodeBoundingBoxes: rects }));
};
export const paintDragLayer = (painter, props, state) => {
    var _a;
    painter.wipe();
    if (!state.dragRegion && ((_a = state.selectedElectrodes) === null || _a === void 0 ? void 0 : _a.length) === 0 && state.draggedElectrodes.length === 0)
        return;
    const regionBrush = { color: 'rgba(127, 127, 127, 0.5)' };
    const selectedElectrodeBrush = { color: 'rgb(0, 0, 192)' };
    const draggedElectrodeBrush = { color: 'rgb(192, 192, 255)' };
    state.selectedElectrodes.forEach(e => {
        painter.fillEllipse(getElectrodeBoundingRect(e, props.electrodeRadius, true), selectedElectrodeBrush);
    });
    state.draggedElectrodes.forEach(e => {
        painter.fillEllipse(getElectrodeBoundingRect(e, props.electrodeRadius, true), draggedElectrodeBrush);
    });
    state.dragRegion && painter.fillRect(state.dragRegion, regionBrush);
};
export const updateDragRegion = (layer, drag) => {
    var _a, _b;
    const { electrodeBoundingBoxes } = layer.getState();
    const hits = electrodeBoundingBoxes.filter((r) => rectangularRegionsIntersect(r.br, drag.dragRect));
    if (drag.released) {
        const currentSelected = drag.shift ? (_b = (_a = layer.getState()) === null || _a === void 0 ? void 0 : _a.selectedElectrodes) !== null && _b !== void 0 ? _b : [] : [];
        layer.setState(Object.assign(Object.assign({}, layer.getState()), { dragRegion: null, draggedElectrodes: [], selectedElectrodes: [...currentSelected, ...hits] }));
    }
    else {
        layer.setState(Object.assign(Object.assign({}, layer.getState()), { dragRegion: drag.dragRect, draggedElectrodes: hits }));
    }
    layer.scheduleRepaint();
};
//# sourceMappingURL=DragLayer.js.map