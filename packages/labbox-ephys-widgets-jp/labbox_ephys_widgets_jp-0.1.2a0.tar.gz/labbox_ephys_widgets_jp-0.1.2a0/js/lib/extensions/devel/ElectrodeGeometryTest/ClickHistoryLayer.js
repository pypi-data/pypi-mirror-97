import { ClickEventType } from '../../common/CanvasWidget/CanvasWidgetLayer';
export const paintClickLayer = (painter, props, state) => {
    var _a;
    painter.wipe();
    (_a = state === null || state === void 0 ? void 0 : state.clickHistory) === null || _a === void 0 ? void 0 : _a.forEach((point, i) => {
        const color = i * 50;
        const pen = { color: `rgb(${color}, 0, 128)`, width: 3 };
        const boundingRect = {
            xmin: point[0] - 5,
            ymin: point[1] - 5,
            xmax: point[0] + 5,
            ymax: point[1] + 5
        };
        painter.drawEllipse(boundingRect, pen);
    });
};
export const handleClickTrail = (e, layer) => {
    if (e.type !== ClickEventType.Press)
        return;
    let clickLayerState = layer.getState();
    const clickHistory = (clickLayerState === null || clickLayerState === void 0 ? void 0 : clickLayerState.clickHistory) || [];
    layer.setState({
        clickHistory: [e.point, ...clickHistory.slice(0, 9)]
    });
    layer.scheduleRepaint();
};
//# sourceMappingURL=ClickHistoryLayer.js.map