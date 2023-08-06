import CanvasWidget from './CanvasWidget';
import { TransformationMatrix, Vec2 } from './Geometry';
export { PainterPath } from './CanvasPainter';
export declare const funcToTransform: (transformation: (p: Vec2) => Vec2) => TransformationMatrix;
export default CanvasWidget;
