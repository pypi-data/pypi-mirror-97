import { CanvasWidgetLayer, DiscreteMouseEventHandler, DragHandler, KeyboardEventHandler, MousePresenceEventHandler, WheelEventHandler } from "../../common/CanvasWidget/CanvasWidgetLayer";
import { TransformationMatrix } from "../../common/CanvasWidget/Geometry";
import { TimeWidgetLayerProps } from "./TimeWidgetLayerProps";
interface LayerState {
    timeRange: {
        min: number;
        max: number;
    } | null;
    transformations: TransformationMatrix[];
    yAxisTransformations: TransformationMatrix[];
    yAxisWidths: number[];
    yAxisHeights: number[];
    inverseTransformations: TransformationMatrix[];
    anchorTimepoint: number | null;
    dragging: boolean;
    captureWheel: boolean;
    paintStatus: {
        paintCode: number;
        completenessFactor: number;
    };
}
export declare const handleClick: DiscreteMouseEventHandler;
export declare const handleMouseOut: MousePresenceEventHandler;
export declare const handleDrag: DragHandler;
export declare const handleWheel: WheelEventHandler;
export declare const handleKeyboardEvent: KeyboardEventHandler;
export declare const createMainLayer: () => CanvasWidgetLayer<TimeWidgetLayerProps, LayerState>;
export {};
