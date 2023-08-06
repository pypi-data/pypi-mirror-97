var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
import { useEffect, useState } from 'react';
import { CanvasPainter } from './CanvasPainter';
import { getInverseTransformationMatrix, transformPoint, transformRect, transformXY } from './Geometry';
export var ClickEventType;
(function (ClickEventType) {
    ClickEventType["Move"] = "MOVE";
    ClickEventType["Press"] = "PRESS";
    ClickEventType["Release"] = "RELEASE";
})(ClickEventType || (ClickEventType = {}));
export var KeyEventType;
(function (KeyEventType) {
    KeyEventType["Press"] = "PRESS";
    KeyEventType["Release"] = "RELEASE";
})(KeyEventType || (KeyEventType = {}));
export var MousePresenceEventType;
(function (MousePresenceEventType) {
    MousePresenceEventType["Enter"] = "ENTER";
    MousePresenceEventType["Leave"] = "LEAVE";
    MousePresenceEventType["Out"] = "OUT";
})(MousePresenceEventType || (MousePresenceEventType = {}));
export const formClickEventFromMouseEvent = (e, t, i) => {
    const element = e.currentTarget;
    let point = [e.clientX - element.getBoundingClientRect().x, e.clientY - element.getBoundingClientRect().y];
    if (i) {
        const pointH = transformXY(i, point[0], point[1]);
        point = [pointH[0], pointH[1]];
    }
    const modifiers = {
        alt: e.altKey,
        ctrl: e.ctrlKey || e.metaKey,
        shift: e.shiftKey,
    };
    return { point: [point[0], point[1]], mouseButton: e.buttons, modifiers: modifiers, type: t };
};
export const formWheelEvent = (e) => {
    return {
        deltaY: e.deltaY
    };
};
export const formKeyboardEvent = (type, e) => {
    return {
        type,
        keyCode: e.keyCode
    };
};
export class CanvasWidgetLayer {
    constructor(onPaint, onPropsChange, initialState, handlers) {
        this._runningOnPropsChange = false;
        this._props = null; // this will be null until props are passed in from the CanvasWidget
        // these will be null until they are set by the CanvasWidget
        this._pixelWidth = null;
        this._pixelHeight = null;
        this._canvasElement = null;
        this._repaintScheduled = false;
        this._lastRepaintTimestamp = Number(new Date());
        this._discreteMouseEventHandlers = [];
        this._dragHandlers = [];
        this._keyboardEventHandlers = [];
        this._mousePresenceEventHandlers = [];
        this._wheelEventHandlers = [];
        this._refreshRate = 120; // Hz
        this._state = initialState;
        this._onPaint = onPaint;
        this._onPropsChange = onPropsChange;
        this._discreteMouseEventHandlers = (handlers === null || handlers === void 0 ? void 0 : handlers.discreteMouseEventHandlers) || [];
        this._dragHandlers = (handlers === null || handlers === void 0 ? void 0 : handlers.dragHandlers) || [];
        this._keyboardEventHandlers = (handlers === null || handlers === void 0 ? void 0 : handlers.keyboardEventHandlers) || [];
        this._mousePresenceEventHandlers = (handlers === null || handlers === void 0 ? void 0 : handlers.mousePresenceEventHandlers) || [];
        this._wheelEventHandlers = (handlers === null || handlers === void 0 ? void 0 : handlers.wheelEventHandlers) || [];
        this._transformMatrix = [[1, 0, 0], [0, 1, 0], [0, 0, 1]];
        this._inverseMatrix = [[1, 0, 0], [0, 1, 0], [0, 0, 1]];
    }
    getProps() {
        if (!this._props)
            throw Error('getProps must not be called before initial props are set');
        return this._props;
    }
    setProps(p) {
        if (this._runningOnPropsChange) {
            throw Error('Calling setProps inside onPropsChange is not allowed.');
        }
        if ((this._props === null) || (!shallowEqual(this._props, p))) {
            this._props = p;
            this._pixelWidth = p.width;
            this._pixelHeight = p.height;
            this._runningOnPropsChange = true;
            try {
                this._onPropsChange(this, p);
            }
            finally {
                this._runningOnPropsChange = false;
            }
        }
    }
    getState() {
        return this._state;
    }
    setState(s) {
        this._state = s;
    }
    getTransformMatrix() {
        return this._transformMatrix;
    }
    setTransformMatrix(t) {
        this._transformMatrix = t;
        try {
            this._inverseMatrix = getInverseTransformationMatrix(t);
        }
        catch (err) {
            console.warn(err);
            console.warn('WARNING: problem getting inverse transformation matrix');
            this._inverseMatrix = t;
        }
    }
    pixelWidth() {
        if (this._pixelWidth === null)
            throw Error('Cannot get pixelWidth before it is set');
        return this._pixelWidth;
    }
    pixelHeight() {
        if (this._pixelHeight === null)
            throw Error('Cannot get pixelHeight before it is set');
        return this._pixelHeight;
    }
    resetCanvasElement(canvasElement) {
        this._canvasElement = canvasElement;
    }
    canvasElement() {
        return this._canvasElement;
    }
    refreshRate() {
        return this._refreshRate;
    }
    setRefreshRate(hz) {
        this._refreshRate = hz;
    }
    scheduleRepaint() {
        if (this._repaintScheduled) {
            return;
        }
        const elapsedSinceLastRepaint = Number(new Date()) - this._lastRepaintTimestamp;
        const refreshDelay = 1000 / this._refreshRate;
        if (elapsedSinceLastRepaint > refreshDelay * 2) {
            // do it right away
            this._doRepaint();
            return;
        }
        this._repaintScheduled = true;
        // const timer = Number(new Date())                 // unused
        setTimeout(() => {
            // let elapsed = Number(new Date()) - timer;    // unused
            this._repaintScheduled = false;
            this._doRepaint();
        }, refreshDelay); // this timeout controls the refresh rate
    }
    repaintImmediate() {
        this._doRepaint();
    }
    _doRepaint() {
        var _a, _b;
        return __awaiter(this, void 0, void 0, function* () {
            const context = (_b = (_a = this._canvasElement) === null || _a === void 0 ? void 0 : _a.getContext('2d')) !== null && _b !== void 0 ? _b : null;
            if (!context)
                return;
            if ((this._pixelWidth === null) || (this._pixelHeight === null))
                return;
            let painter = new CanvasPainter(context, this._pixelWidth, this._pixelHeight, this._transformMatrix);
            // painter.clear()
            // _onPaint may or may not be async
            const promise = this._onPaint(painter, this._props, this._state);
            if (promise) {
                // if returned a promise, it was async, and let's await
                // in this case we should update the lastRepaintTimestamp both before and after the paint
                this._lastRepaintTimestamp = Number(new Date());
                yield promise;
            }
            // this.unclipToSelf(ctx)
            this._lastRepaintTimestamp = Number(new Date());
        });
    }
    handleDiscreteEvent(e, type) {
        if (this._discreteMouseEventHandlers.length === 0)
            return;
        const click = formClickEventFromMouseEvent(e, type, this._inverseMatrix);
        // Don't respond to events outside the layer
        // NB possible minor efficiency gain if we cache our bounding coordinates in pixelspace.
        // if (!pointInRect(click.point, this.getCoordRange())) return
        for (let fn of this._discreteMouseEventHandlers) {
            fn(click, this);
        }
    }
    handleDrag(pixelDragRect, released, shift, pixelAnchor, pixelPosition) {
        if (this._dragHandlers.length === 0)
            return;
        const coordDragRect = transformRect(this._inverseMatrix, pixelDragRect);
        // if (!rectangularRegionsIntersect(coordDragRect, this.getCoordRange())) return // short-circuit if event is nothing to do with us
        // Note: append a 1 to make the Vec2s into Vec2Hs
        const coordAnchor = pixelAnchor ? transformPoint(this._inverseMatrix, [...pixelAnchor, 1]) : undefined;
        const coordPosition = pixelPosition ? transformPoint(this._inverseMatrix, [...pixelPosition, 1]) : undefined;
        for (let fn of this._dragHandlers) {
            fn(this, { dragRect: coordDragRect, released: released, shift: shift || false, anchor: coordAnchor, position: coordPosition });
        }
    }
    handleKeyboardEvent(type, e) {
        if (this._keyboardEventHandlers.length === 0)
            return true;
        const keyboardEvent = formKeyboardEvent(type, e);
        let passEventBackToUi = true;
        for (let fn of this._keyboardEventHandlers) {
            if (fn(keyboardEvent, this) === false)
                passEventBackToUi = false;
        }
        return passEventBackToUi;
    }
    handleMousePresenceEvent(e, type) {
        if (this._mousePresenceEventHandlers.length === 0)
            return;
        const presenceEvent = { type: type };
        for (let fn of this._mousePresenceEventHandlers) {
            fn(presenceEvent, this);
        }
    }
    handleWheelEvent(e) {
        if (this._wheelEventHandlers.length === 0)
            return;
        const wheelEvent = formWheelEvent(e);
        for (let fn of this._wheelEventHandlers) {
            fn(wheelEvent, this);
        }
    }
}
export const useLayer = (createLayer, layerProps) => {
    const [layer, setLayer] = useState(null);
    useEffect(() => {
        if (layer === null) {
            setLayer(createLayer());
        }
    }, [layer, setLayer, createLayer]);
    if ((layer) && (layerProps)) {
        layer.setProps(layerProps);
    }
    return layer;
};
const listsMatch = (list1, list2) => {
    if (list1.length !== list2.length)
        return false;
    for (let i = 0; i < list1.length; i++) {
        if (list1[i] !== list2[i])
            return false;
    }
    return true;
};
export const useLayers = (layers) => {
    const [prevLayers, setPrevLayers] = useState([]);
    if (listsMatch(prevLayers, layers)) {
        return prevLayers;
    }
    else {
        setPrevLayers(layers);
        return layers;
    }
};
// export const useLayers = <LayerProps extends BaseLayerProps>(layerList: (CanvasWidgetLayer<LayerProps, any> | null)[]): CanvasWidgetLayer<LayerProps, any>[] | null => {
//     const [layers, setLayers] = useState<CanvasWidgetLayer<LayerProps, Object>[] | null>(null)
//     useEffect(() => {
//         if (layers === null) {
//             if (layerList.filter(L => (L === null)).length === 0) {
//                 const layerList2: CanvasWidgetLayer<LayerProps, any>[] = []
//                 layerList.forEach(L => {
//                     if (L === null) throw Error('Unexpected null layer')
//                     layerList2.push(L)
//                 })
//                 setLayers(layerList2)
//             }
//         }
//     }, [layers, setLayers, layerList])
//     return layers
// }
const shallowEqual = (x, y) => {
    for (let k in x) {
        if (x[k] !== y[k]) {
            return false;
        }
    }
    for (let k in y) {
        if (x[k] !== y[k]) {
            return false;
        }
    }
    return true;
};
//# sourceMappingURL=CanvasWidgetLayer.js.map