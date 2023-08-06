import { RectangularRegion, TransformationMatrix, Vec2 } from './Geometry';
export interface TextAlignment {
    Horizontal: 'AlignLeft' | 'AlignCenter' | 'AlignRight';
    Vertical: 'AlignTop' | 'AlignCenter' | 'AlignBottom';
}
export declare const isTextAlignment: (x: any) => x is TextAlignment;
export declare type TextOrientation = 'Horizontal' | 'Vertical';
export declare type Context2D = CanvasRenderingContext2D | OffscreenCanvasRenderingContext2D;
declare type Color = 'black' | 'red' | 'blue' | 'transparent' | string;
export interface Pen {
    color: Color;
    width?: number;
}
export interface Font {
    pixelSize: number;
    family: 'Arial' | string;
}
export interface Brush {
    color: Color;
}
export declare const isBrush: (x: any) => x is Brush;
export declare class CanvasPainter {
    _exportingFigure: boolean;
    _context2D: CanvasRenderingContext2D | OffscreenCanvasRenderingContext2D;
    _pixelWidth: number;
    _pixelHeight: number;
    _primaryContext2D: CanvasRenderingContext2D | OffscreenCanvasRenderingContext2D;
    _offscreenCanvas: OffscreenCanvas | null;
    _transformMatrix: TransformationMatrix;
    constructor(context2d: Context2D, pixelWidth: number, pixelHeight: number, transformMatrix: TransformationMatrix);
    transform(m: TransformationMatrix): CanvasPainter;
    useOffscreenCanvas(W: number, H: number): void;
    transferOffscreenToPrimary(): void;
    getDefaultPen(): {
        color: string;
    };
    getDefaultFont(): {
        "pixel-size": number;
        family: string;
    };
    getDefaultBrush(): {
        color: string;
    };
    createPainterPath(): PainterPath;
    setExportingFigure(val: boolean): void;
    exportingFigure(): boolean;
    fillWholeCanvas(color: Color): void;
    clear(): void;
    clearRect(rect: RectangularRegion): void;
    ctxSave(): void;
    ctxRestore(): void;
    wipe(): void;
    ctxTranslate(dx: number | Vec2, dy?: number | undefined): void;
    ctxRotate(theta: number): void;
    fillRect(rect: RectangularRegion, brush: Brush): void;
    drawRect(rect: RectangularRegion, pen: Pen): void;
    getEllipseFromBoundingRect(boundingRect: RectangularRegion): {
        center: Vec2;
        W: number;
        H: number;
    };
    fillEllipse(boundingRect: RectangularRegion, brush: Brush): void;
    drawEllipse(boundingRect: RectangularRegion, pen: Pen): void;
    drawPath(painterPath: PainterPath, pen: Pen): void;
    drawLine(x1: number, y1: number, x2: number, y2: number, pen: Pen): void;
    drawText({ text, rect, alignment, font, pen, brush, orientation }: {
        text: string;
        rect: RectangularRegion;
        alignment: TextAlignment;
        font: Font;
        pen: Pen;
        brush: Brush;
        orientation?: TextOrientation;
    }): void;
    drawMarker(center: Vec2, opts: {
        radius: number;
        pen?: Pen;
        brush?: Brush;
    }): void;
}
interface PainterPathAction {
    name: 'moveTo' | 'lineTo';
    x: number | undefined;
    y: number | undefined;
}
export declare class PainterPath {
    _actions: PainterPathAction[];
    moveTo(x: number | Vec2, y?: number | undefined): void;
    lineTo(x: number | Vec2, y?: number | undefined): void;
    _draw(ctx: Context2D, tmatrix: TransformationMatrix): void;
    _applyAction(ctx: Context2D, a: PainterPathAction): void;
    _transformPathPoints(tmatrix: TransformationMatrix): PainterPathAction[];
}
export {};
