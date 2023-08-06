import CanvasWidget from './CanvasWidget';
export { PainterPath } from './CanvasPainter';
export const funcToTransform = (transformation) => {
    const p00 = transformation([0, 0]);
    const p10 = transformation([1, 0]);
    const p01 = transformation([0, 1]);
    const M = [
        [p10[0] - p00[0], p01[0] - p00[0], p00[0]],
        [p10[1] - p00[1], p01[1] - p00[1], p00[1]],
        [0, 0, 1]
    ];
    return M;
};
export default CanvasWidget;
//# sourceMappingURL=index.js.map