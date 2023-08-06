import { funcToTransform } from '../../common/CanvasWidget';
import { CanvasWidgetLayer } from "../../common/CanvasWidget/CanvasWidgetLayer";
const initialLayerState = {};
const onPaint = (painter, layerProps, state) => {
    const { panels, height, margins } = layerProps;
    if (panels.length === 0)
        return;
    painter.wipe();
    for (let i = 0; i < panels.length; i++) {
        const transformation = funcToTransform((p) => {
            const xfrac = p[0];
            const yfrac = (i / panels.length) + p[1] * (1 / panels.length);
            const x = 0 + xfrac * margins.left;
            const y = height - margins.bottom - yfrac * (height - margins.bottom - margins.top);
            return [x, y];
        });
        const painter2 = painter.transform(transformation);
        const label = panels[i].label();
        let rect = { xmin: 0.2, ymin: 0.2, xmax: 0.6, ymax: 0.6 };
        let alignment = { Horizontal: 'AlignRight', Vertical: "AlignCenter" };
        const font = { pixelSize: 12, family: 'Arial' };
        painter2.drawText({
            rect, alignment, font, pen: { color: 'black' }, brush: { color: 'black' }, text: label
        });
    }
};
const onPropsChange = (layer, layerProps) => {
};
export const createPanelLabelLayer = () => {
    return new CanvasWidgetLayer(onPaint, onPropsChange, initialLayerState);
};
//# sourceMappingURL=panelLabelLayer.js.map