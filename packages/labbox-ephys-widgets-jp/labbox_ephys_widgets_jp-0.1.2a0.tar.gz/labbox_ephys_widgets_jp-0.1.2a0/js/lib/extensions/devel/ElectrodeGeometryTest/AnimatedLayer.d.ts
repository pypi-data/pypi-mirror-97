import { CanvasPainter } from '../../common/CanvasWidget/CanvasPainter';
import { DiscreteMouseEventHandler } from '../../common/CanvasWidget/CanvasWidgetLayer';
import { Vec2 } from '../../common/CanvasWidget/Geometry';
import { ElectrodeLayerProps } from './ElectrodeGeometry';
interface AnimationPoint {
    loc: Vec2;
    start: DOMHighResTimeStamp;
    end: DOMHighResTimeStamp;
    pct: number;
    done: boolean;
}
export interface AnimatedLayerState {
    points: AnimationPoint[];
    newQueue: AnimationPoint[];
}
export declare const paintAnimationLayer: (painter: CanvasPainter, props: ElectrodeLayerProps, state: AnimatedLayerState) => void;
export declare const handleAnimatedClick: DiscreteMouseEventHandler;
export {};
