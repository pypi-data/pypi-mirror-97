import { CanvasPainter } from '../../common/CanvasWidget/CanvasPainter';
import { DiscreteMouseEventHandler } from '../../common/CanvasWidget/CanvasWidgetLayer';
import { Vec2 } from '../../common/CanvasWidget/Geometry';
import { ElectrodeLayerProps } from './ElectrodeGeometry';
export declare type ClickHistoryState = {
    clickHistory: Vec2[];
};
export declare const paintClickLayer: (painter: CanvasPainter, props: ElectrodeLayerProps, state: ClickHistoryState) => void;
export declare const handleClickTrail: DiscreteMouseEventHandler;
