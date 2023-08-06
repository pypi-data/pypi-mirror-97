import { funcToTransform } from '../../common/CanvasWidget';
import { CanvasWidgetLayer } from "../../common/CanvasWidget/CanvasWidgetLayer";
const initialLayerState = {};
const onPaint = (painter, layerProps, state) => {
    const { currentTime, timeRange, width, height, margins } = layerProps;
    if (!timeRange)
        return;
    painter.wipe();
    if (currentTime === null)
        return;
    if (currentTime < timeRange.min)
        return;
    if (currentTime > timeRange.max)
        return;
    const pen = { color: 'blue', width: 2 };
    const transformation = funcToTransform((p) => {
        const xfrac = (p[0] - timeRange.min) / (timeRange.max - timeRange.min);
        const yfrac = p[1];
        const x = margins.left + xfrac * (width - margins.left - margins.right);
        const y = height - margins.bottom - yfrac * (height - margins.bottom - margins.top);
        return [x, y];
    });
    const painter2 = painter.transform(transformation);
    painter2.drawLine(currentTime, 0, currentTime, 1, pen);
};
const onPropsChange = (layer, layerProps) => {
    // layer.scheduleRepaint()
    layer.repaintImmediate();
};
export const createCursorLayer = () => {
    return new CanvasWidgetLayer(onPaint, onPropsChange, initialLayerState);
};
//# sourceMappingURL=cursorLayer.js.map