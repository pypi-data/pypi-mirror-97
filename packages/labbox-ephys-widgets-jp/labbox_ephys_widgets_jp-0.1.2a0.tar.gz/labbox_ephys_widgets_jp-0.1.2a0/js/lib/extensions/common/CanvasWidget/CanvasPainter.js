import { matrix, multiply } from 'mathjs';
import { getCenter, getHeight, getWidth, isNumber, isString, isVec2, isVec3, isVec4, toTransformationMatrix, transformPoint, transformRect } from './Geometry';
export const isTextAlignment = (x) => {
    switch (x.Horizontal) {
        case 'AlignLeft':
        case 'AlignCenter':
        case 'AlignRight':
            break;
        default:
            return false;
    }
    switch (x.Vertical) {
        case 'AlignTop':
        case 'AlignCenter':
        case 'AlignBottom':
            break;
        default:
            return false;
    }
    return true;
};
const rotateRect = (r) => {
    // Corresponds to a 90-degree (counterclockwise) rotation around the origin.
    // A rectangle in quadrant I will wind up in quadrant II lying on its left side, etc.
    return { xmin: -r.ymax, xmax: -r.ymin, ymin: r.xmin, ymax: r.xmax };
};
const rotateTextAlignment = (a) => {
    return {
        Horizontal: a.Vertical === 'AlignBottom' ? 'AlignLeft' : (a.Vertical === 'AlignTop' ? 'AlignRight' : 'AlignCenter'),
        Vertical: a.Horizontal === 'AlignRight' ? 'AlignBottom' : (a.Horizontal === 'AlignLeft' ? 'AlignTop' : 'AlignCenter'),
    };
};
const getTextAlignmentConfig = (rect, alignment) => {
    let x, y;
    let textAlign = 'left';
    let textBaseline = 'bottom';
    switch (alignment.Horizontal) {
        case 'AlignLeft':
            x = rect.xmin;
            textAlign = 'left';
            break;
        case 'AlignCenter':
            x = getCenter(rect)[0];
            textAlign = 'center';
            break;
        case 'AlignRight':
            x = rect.xmax;
            textAlign = 'right';
            break;
        default: // can't happen
            throw new Error('Missing horizontal alignment in drawText: AlignLeft, AlignCenter, or AlignRight');
    }
    switch (alignment.Vertical) {
        case 'AlignBottom':
            y = rect.ymax;
            textBaseline = 'bottom';
            break;
        case 'AlignCenter':
            y = getCenter(rect)[1];
            textBaseline = 'middle';
            break;
        case 'AlignTop':
            y = rect.ymin;
            textBaseline = 'top';
            break;
        default: // can't happen
            throw new Error('Missing vertical alignment in drawText: AlignTop, AlignBottom, or AlignVCenter');
    }
    return { x: x, y: y, textAlign: textAlign, textBaseline: textBaseline };
};
export const isBrush = (x) => {
    if (!x)
        return false;
    if (typeof (x) !== 'object')
        return false;
    if (!('color' in x))
        return false;
    return true;
};
export class CanvasPainter {
    constructor(context2d, pixelWidth, pixelHeight, transformMatrix) {
        this._exportingFigure = false;
        this._offscreenCanvas = null;
        this._context2D = context2d;
        this._primaryContext2D = context2d;
        this._pixelWidth = pixelWidth;
        this._pixelHeight = pixelHeight;
        this._transformMatrix = transformMatrix;
    }
    // Return a new, transformed painter
    transform(m) {
        // todo: figure out whether this should be left or right-multiplication
        try {
            const m2 = toTransformationMatrix(multiply(matrix(this._transformMatrix), matrix(m)));
            return new CanvasPainter(this._context2D, this._pixelWidth, this._pixelHeight, m2);
        }
        catch (err) {
            console.warn('Problem transforming painter:', err);
            return this;
        }
    }
    useOffscreenCanvas(W, H) {
        try {
            const c = new OffscreenCanvas(Math.max(W, 10), Math.max(H, 10));
            this._offscreenCanvas = c;
            const cc = c.getContext('2d');
            if (!cc)
                throw Error('Unexpected');
            this._context2D = cc;
        }
        catch (err) {
            console.warn('Problem in useOffscreenCanvas', err);
        }
    }
    transferOffscreenToPrimary() {
        const c = this._offscreenCanvas;
        if (!c) {
            console.warn('No offscreen canvas');
            return;
        }
        const image = c.transferToImageBitmap();
        this._context2D = this._primaryContext2D;
        this._context2D.clearRect(0, 0, image.width, image.height);
        this._context2D.drawImage(image, 0, 0);
    }
    // TODO: Delete these default methods?
    getDefaultPen() {
        return { color: 'black' };
    }
    getDefaultFont() {
        return { "pixel-size": 12, family: 'Arial' };
    }
    getDefaultBrush() {
        return { color: 'black' };
    }
    createPainterPath() {
        return new PainterPath();
    }
    setExportingFigure(val) {
        this._exportingFigure = val;
    }
    exportingFigure() {
        return this._exportingFigure;
    }
    // This is a log function, basically just for debugging purposes.
    fillWholeCanvas(color) {
        console.log(`Pixel dimensions: 0 to ${this._pixelWidth} and 0 to ${this._pixelHeight}`);
        this._context2D.save();
        applyBrush(this._context2D, { color: color });
        this._context2D.fillRect(0, 0, this._pixelWidth, this._pixelHeight);
        this._context2D.restore();
    }
    clear() {
        this.clearRect({ xmin: 0, xmax: this._pixelWidth, ymin: 0, ymax: this._pixelHeight });
    }
    clearRect(rect) {
        this.fillRect(rect, { color: 'transparent' });
    }
    ctxSave() {
        this._context2D.save();
    }
    ctxRestore() {
        this._context2D.restore();
    }
    wipe() {
        // const pr = transformRect(this._transformMatrix, this._fullDimensions)
        // this._context2D.clearRect(pr.xmin, pr.ymin, getWidth(pr), getHeight(pr));
        this._context2D.clearRect(0, 0, this._pixelWidth, this._pixelHeight);
    }
    // TODO: REWRITE THIS ctxTranslate
    ctxTranslate(dx, dy = undefined) {
        throw Error('Deprecated method, needs rewrite.');
        // if (dy === undefined) {
        //     if (typeof dx === 'number') {
        //         throw Error('unexpected');
        //     }
        //     let tmp = dx;
        //     dx = tmp[0];
        //     dy = tmp[1];
        //     this._context2D.translate(dx, dy);
        // }
        // if (typeof dx === 'object') {
        //     throw Error('Bad signature: dx object and dy not undef: ctxTranslate')
        // }
        // this._context2D.translate(dx, dy);
    }
    ctxRotate(theta) {
        this._context2D.rotate(theta);
    }
    fillRect(rect, brush) {
        const pr = transformRect(this._transformMatrix, rect); // covert rect to pixelspace
        // console.log(`Transformed ${JSON.stringify(rect)} to ${JSON.stringify(pr)}`)
        // console.log(`Measure (pixelspace) width: ${getWidth(pr)}, height: ${getHeight(pr)}`)
        this._context2D.save();
        applyBrush(this._context2D, brush);
        // NOTE: Due to the pixelspace-conversion axis flip, the height should be negative.
        this._context2D.fillRect(Math.min(pr.xmin, pr.xmax), Math.min(pr.ymin, pr.ymax), getWidth(pr), getHeight(pr));
        this._context2D.restore();
    }
    drawRect(rect, pen) {
        const pr = transformRect(this._transformMatrix, rect); // convert rect to pixelspace
        this._context2D.save();
        applyPen(this._context2D, pen);
        // NOTE: Due to the pixelspace-conversion axis flip, the height should be negative.
        this._context2D.strokeRect(Math.min(pr.xmin, pr.xmax), Math.min(pr.ymin, pr.ymax), getWidth(pr), getHeight(pr));
        this._context2D.restore();
    }
    getEllipseFromBoundingRect(boundingRect) {
        const r = transformRect(this._transformMatrix, boundingRect);
        const center = getCenter(r);
        const W = Math.abs(getWidth(r));
        const H = Math.abs(getHeight(r));
        return { center, W, H };
    }
    fillEllipse(boundingRect, brush) {
        const { center, W, H } = Object.assign({}, this.getEllipseFromBoundingRect(boundingRect));
        // this._context2D.save()
        this._context2D.fillStyle = toColorStr(brush.color);
        this._context2D.beginPath();
        this._context2D.ellipse(center[0], center[1], W / 2, H / 2, 0, 0, 2 * Math.PI);
        this._context2D.fill();
        // this._context2D.restore()
    }
    drawEllipse(boundingRect, pen) {
        const { center, W, H } = Object.assign({}, this.getEllipseFromBoundingRect(boundingRect));
        this._context2D.save();
        applyPen(this._context2D, pen);
        // console.log(`Attempting to draw ellipse: ${center[0]} ${center[1]} ${W/2} ${H/2}`)
        this._context2D.beginPath();
        this._context2D.ellipse(center[0], center[1], W / 2, H / 2, 0, 0, 2 * Math.PI);
        this._context2D.stroke();
        this._context2D.restore();
    }
    drawPath(painterPath, pen) {
        this._context2D.save();
        applyPen(this._context2D, pen);
        painterPath._draw(this._context2D, this._transformMatrix);
        this._context2D.restore();
    }
    drawLine(x1, y1, x2, y2, pen) {
        const pPath = new PainterPath();
        pPath.moveTo(x1, y1);
        pPath.lineTo(x2, y2);
        this.drawPath(pPath, pen);
    }
    drawText({ text, rect, alignment, font, pen, brush, orientation = 'Horizontal' }) {
        let rect2 = transformRect(this._transformMatrix, rect);
        this._context2D.save();
        if (orientation === 'Vertical') {
            this._context2D.rotate(-Math.PI / 2);
            rect2 = rotateRect(rect2);
            alignment = rotateTextAlignment(alignment);
        }
        // the following is useful for debugging the text placement, especially when orientation is Vertical
        // applyPen(this._context2D, {color: 'green'})
        // this._context2D.strokeRect(Math.min(rect2.xmin, rect2.xmax), Math.min(rect2.ymin, rect2.ymax), getWidth(rect2), getHeight(rect2))
        // this._context2D.strokeRect(Math.min(rect2.xmin, rect2.xmax) + 5, Math.min(rect2.ymin, rect2.ymax) + 5, getWidth(rect2) - 10, getHeight(rect2) - 10)
        applyFont(this._context2D, font);
        const config = getTextAlignmentConfig(rect2, alignment);
        applyTextAlignment(this._context2D, config);
        applyPen(this._context2D, pen);
        applyBrush(this._context2D, brush);
        this._context2D.translate(config.x, config.y);
        this._context2D.fillText(text, 0, 0);
        this._context2D.restore();
    }
    drawMarker(center, opts) {
        const p = transformPoint(this._transformMatrix, center);
        this._context2D.save();
        if (opts.pen) {
            applyPen(this._context2D, opts.pen);
            this._context2D.beginPath();
            this._context2D.ellipse(p[0], p[1], opts.radius, opts.radius, 0, 0, 2 * Math.PI);
            this._context2D.stroke();
        }
        if (opts.brush) {
            applyBrush(this._context2D, opts.brush);
            this._context2D.beginPath();
            this._context2D.ellipse(p[0], p[1], opts.radius, opts.radius, 0, 0, 2 * Math.PI);
            this._context2D.fill();
        }
        this._context2D.restore();
    }
}
export class PainterPath {
    constructor() {
        this._actions = [];
    }
    moveTo(x, y = undefined) {
        if (isVec2(x)) {
            return this.moveTo(x[0], x[1]);
        }
        if (!isNumber(y))
            throw Error('unexpected');
        this._actions.push({
            name: 'moveTo',
            x,
            y
        });
    }
    lineTo(x, y = undefined) {
        if (isVec2(x)) {
            return this.lineTo(x[0], x[1]);
        }
        if (!isNumber(y))
            throw Error('unexpected');
        this._actions.push({
            name: 'lineTo',
            x,
            y
        });
    }
    _draw(ctx, tmatrix) {
        ctx.beginPath();
        const actions = this._transformPathPoints(tmatrix);
        actions.forEach(a => {
            this._applyAction(ctx, a);
        });
        ctx.stroke();
    }
    _applyAction(ctx, a) {
        if (a.name === 'moveTo') {
            a.x !== undefined && a.y !== undefined && ctx.moveTo(a.x, a.y);
        }
        else if (a.name === 'lineTo') {
            a.x !== undefined && a.y !== undefined && ctx.lineTo(a.x, a.y);
        }
    }
    _transformPathPoints(tmatrix) {
        const A = matrix(tmatrix);
        // if the paths were long it might be more efficient to make the vectors a wide matrix
        // ...but honestly it's probably so small a thing for what we do that it matters not
        return this._actions.map((a) => {
            if ((a.x !== undefined) && (a.y !== undefined)) {
                const x = matrix([a.x, a.y, 1]);
                const b = multiply(A, x).toArray();
                return Object.assign(Object.assign({}, a), { x: b[0], y: b[1] });
            }
            else {
                return a;
            }
        });
    }
}
const toColorStr = (col) => {
    // TODO: Could do more validity checking here
    if (isString(col))
        return col;
    else if (isVec4(col)) {
        return (`rgba(${Math.floor(col[0])}, ${Math.floor(col[1])}, ${Math.floor(col[2])}, ${col[3]})`);
    }
    else if (isVec3(col)) {
        return (`rgb(${Math.floor(col[0])}, ${Math.floor(col[1])}, ${Math.floor(col[2])})`);
    }
    else {
        throw Error('unexpected');
    }
};
const applyPen = (ctx, pen) => {
    const color = pen.color || 'black';
    const lineWidth = (isNumber(pen.width)) ? pen.width : 1;
    ctx.strokeStyle = toColorStr(color);
    ctx.lineWidth = lineWidth || 1;
};
const applyBrush = (ctx, brush) => {
    const color = 'color' in brush ? brush.color : 'black';
    ctx.fillStyle = toColorStr(color);
};
const applyFont = (ctx, font) => {
    const size = font.pixelSize || '12';
    const face = font.family || 'Arial';
    ctx.font = `${size}px ${face}`;
};
const applyTextAlignment = (ctx, alignment) => {
    ctx.textAlign = alignment.textAlign;
    ctx.textBaseline = alignment.textBaseline;
};
//# sourceMappingURL=CanvasPainter.js.map