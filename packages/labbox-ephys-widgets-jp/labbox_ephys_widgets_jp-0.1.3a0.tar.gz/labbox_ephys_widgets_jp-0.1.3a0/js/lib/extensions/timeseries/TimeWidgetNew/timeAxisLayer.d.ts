import { CanvasWidgetLayer } from "../../common/CanvasWidget/CanvasWidgetLayer";
import { TransformationMatrix } from "../../common/CanvasWidget/Geometry";
import { TimeWidgetLayerProps } from "./TimeWidgetLayerProps";
interface LayerState {
    transformation: TransformationMatrix;
    inverseTransformation: TransformationMatrix;
}
export declare const createTimeAxisLayer: () => CanvasWidgetLayer<TimeWidgetLayerProps, LayerState>;
export {};
