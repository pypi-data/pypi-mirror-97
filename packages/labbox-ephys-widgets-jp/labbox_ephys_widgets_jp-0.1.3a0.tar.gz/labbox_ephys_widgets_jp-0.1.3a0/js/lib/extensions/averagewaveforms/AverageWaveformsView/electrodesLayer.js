import { CanvasWidgetLayer, ClickEventType } from "../../common/CanvasWidget/CanvasWidgetLayer";
import { pointIsInEllipse, rectangularRegionsIntersect } from '../../common/CanvasWidget/Geometry';
import setupElectrodes from './setupElectrodes';
const initialLayerState = {
    electrodeBoxes: [],
    radius: 0,
    pixelRadius: 0,
    dragRegion: null,
    draggedElectrodeIds: [],
    hoveredElectrodeId: null
};
const defaultColors = {
    border: 'rgb(30, 30, 30)',
    base: 'rgb(0, 0, 255)',
    selected: 'rgb(196, 196, 128)',
    hover: 'rgb(128, 128, 255)',
    selectedHover: 'rgb(200, 200, 196)',
    dragged: 'rgb(0, 0, 196)',
    draggedSelected: 'rgb(180, 180, 150)',
    dragRect: 'rgba(196, 196, 196, 0.5)',
    textLight: 'rgb(228, 228, 228)',
    textDark: 'rgb(32, 32, 32)'
};
const handleClick = (event, layer) => {
    if (event.type !== ClickEventType.Release)
        return;
    const { selectionDispatch, electrodeOpts: opts } = layer.getProps();
    if (opts.disableSelection)
        return;
    const state = layer.getState();
    if (state === null)
        return;
    const hitIds = state.electrodeBoxes.filter((r) => pointIsInEllipse(event.point, [r.x, r.y], state.radius)).map(r => r.id);
    // handle clicks that weren't on an electrode
    if (hitIds.length === 0) {
        if (!(event.modifiers.ctrl || event.modifiers.shift || state.dragRegion)) {
            // simple-click that doesn't select anything should deselect everything. Shift- or Ctrl-clicks on empty space do nothing.
            selectionDispatch({ type: 'SetSelectedElectrodeIds', selectedElectrodeIds: [] });
        }
        return;
    }
    // Our definition of radius precludes any two electrodes from overlapping, so hitIds should have 0 or 1 elements.
    // Since we've already handled the case where it's 0, now it must be 1.
    const hitId = hitIds[0];
    const currentSelection = layer.getProps().selection.selectedElectrodeIds || [];
    const newSelection = event.modifiers.ctrl // ctrl-click: toggle state of clicked item
        ? currentSelection.includes(hitId)
            ? currentSelection.filter(id => id !== hitId)
            : [...currentSelection, hitId]
        : event.modifiers.shift
            ? [...currentSelection, hitId] // shift-click: add selected item unconditionally
            : [hitId]; // simple click: clear all selections except clicked item
    selectionDispatch({ type: 'SetSelectedElectrodeIds', selectedElectrodeIds: newSelection });
    layer.scheduleRepaint();
};
const handleHover = (event, layer) => {
    if (event.type !== ClickEventType.Move)
        return;
    const state = layer.getState();
    if (state === null)
        return;
    const hoveredIds = state.electrodeBoxes.filter((r) => pointIsInEllipse(event.point, [r.x, r.y], state.radius)).map(r => r.id);
    layer.setState(Object.assign(Object.assign({}, state), { hoveredElectrodeId: hoveredIds.length === 0 ? null : hoveredIds[0] }));
    layer.scheduleRepaint();
};
const handleDragSelect = (layer, drag) => {
    var _a, _b, _c;
    const state = layer.getState();
    const { selectionDispatch, electrodeOpts: opts } = layer.getProps();
    if (opts.disableSelection)
        return;
    if (state === null)
        return; // state not set; can't happen but keeps linter happy
    const hits = (_a = state.electrodeBoxes.filter((r) => rectangularRegionsIntersect(r.rect, drag.dragRect))) !== null && _a !== void 0 ? _a : [];
    if (drag.released) {
        const currentSelected = drag.shift ? (_c = (_b = layer.getProps()) === null || _b === void 0 ? void 0 : _b.selection.selectedElectrodeIds) !== null && _c !== void 0 ? _c : [] : [];
        selectionDispatch({ type: 'SetSelectedElectrodeIds', selectedElectrodeIds: [...currentSelected, ...hits.map(r => r.id)] });
        layer.setState(Object.assign(Object.assign({}, state), { dragRegion: null, draggedElectrodeIds: [] }));
    }
    else {
        layer.setState(Object.assign(Object.assign({}, state), { dragRegion: drag.dragRect, draggedElectrodeIds: hits.map(r => r.id) }));
    }
    layer.scheduleRepaint();
};
export const createElectrodesLayer = () => {
    const onPaint = (painter, props, state) => {
        var _a, _b;
        const opts = props.electrodeOpts;
        const colors = opts.colors || defaultColors;
        const showLabels = opts.showLabels;
        painter.wipe();
        const useLabels = state.pixelRadius > 5;
        for (let e of state.electrodeBoxes) {
            const selected = (!opts.disableSelection) && (((_a = props.selection.selectedElectrodeIds) === null || _a === void 0 ? void 0 : _a.includes(e.id)) || false);
            const hovered = (!opts.disableSelection) && (state.hoveredElectrodeId === e.id);
            const dragged = (!opts.disableSelection) && (((_b = state.draggedElectrodeIds) === null || _b === void 0 ? void 0 : _b.includes(e.id)) || false);
            const color = selected
                ? dragged
                    ? colors.draggedSelected
                    : hovered
                        ? colors.selectedHover
                        : colors.selectedHover
                : dragged
                    ? colors.dragged
                    : hovered
                        ? colors.hover
                        : colors.base;
            const layoutMode = props.layoutMode;
            if (layoutMode === 'geom') {
                painter.fillEllipse(e.rect, { color: color });
                painter.drawEllipse(e.rect, { color: colors.border });
            }
            else if (layoutMode === 'vertical') {
                painter.drawLine(e.rect.xmin, (e.rect.ymin + e.rect.ymax) / 2, e.rect.xmax, (e.rect.ymin + e.rect.ymax) / 2, { color: colors.border });
            }
            if (useLabels) {
                const fontColor = ([colors.selected, colors.draggedSelected, colors.hover, colors.selectedHover].includes(color)) ? colors.textDark : colors.textLight;
                if (showLabels) {
                    painter.drawText({
                        rect: e.rect,
                        alignment: { Horizontal: 'AlignCenter', Vertical: 'AlignCenter' },
                        font: { pixelSize: state.pixelRadius, family: 'Arial' },
                        pen: { color: fontColor },
                        brush: { color: fontColor },
                        text: e.label
                    });
                }
            }
        }
        state.dragRegion && painter.fillRect(state.dragRegion, { color: colors.dragRect });
    };
    const onPropsChange = (layer, props) => {
        const state = layer.getState();
        const { width, height, electrodeLocations, electrodeIds, layoutMode } = props;
        const { electrodeBoxes, transform, radius, pixelRadius } = setupElectrodes({ width, height, electrodeLocations, electrodeIds, layoutMode, maxElectrodePixelRadius: props.electrodeOpts.maxElectrodePixelRadius });
        layer.setTransformMatrix(transform);
        layer.setState(Object.assign(Object.assign({}, state), { electrodeBoxes, radius, pixelRadius }));
        layer.scheduleRepaint();
    };
    return new CanvasWidgetLayer(onPaint, onPropsChange, initialLayerState, {
        discreteMouseEventHandlers: [handleClick, handleHover],
        dragHandlers: [handleDragSelect],
    });
};
//# sourceMappingURL=electrodesLayer.js.map