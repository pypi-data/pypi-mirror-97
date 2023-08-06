import { CanvasPainter } from '../../common/CanvasWidget/CanvasPainter';
import { DiscreteMouseEventHandler, DragHandler } from '../../common/CanvasWidget/CanvasWidgetLayer';
import { ElectrodeLayerProps } from './ElectrodeGeometry';
export declare const paintTestLayer: (painter: CanvasPainter, props: ElectrodeLayerProps) => void;
export declare const reportMouseMove: DiscreteMouseEventHandler;
export declare const reportMouseClick: DiscreteMouseEventHandler;
export declare const reportMouseDrag: DragHandler;
