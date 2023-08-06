/// <reference types="react" />
import { CanvasPainter } from './CanvasPainter';
import { RectangularRegion, TransformationMatrix, Vec2 } from './Geometry';
declare type OnPaint<T extends BaseLayerProps, T2 extends object> = (painter: CanvasPainter, layerProps: T, state: T2) => Promise<void> | void;
declare type OnPropsChange<T extends BaseLayerProps> = (layer: CanvasWidgetLayer<T, any>, layerProps: T) => void;
export interface BaseLayerProps {
    width: number;
    height: number;
}
export interface ClickEvent {
    point: Vec2;
    mouseButton: number;
    modifiers: ClickEventModifiers;
    type: ClickEventType;
}
export interface ClickEventModifiers {
    alt?: boolean;
    ctrl?: boolean;
    shift?: boolean;
}
export declare enum ClickEventType {
    Move = "MOVE",
    Press = "PRESS",
    Release = "RELEASE"
}
export declare type ClickEventTypeStrings = keyof typeof ClickEventType;
export interface CanvasDragEvent {
    dragRect: RectangularRegion;
    released: boolean;
    shift: boolean;
    anchor?: Vec2;
    position?: Vec2;
}
export interface KeyboardEvent {
    type: KeyEventType;
    keyCode: number;
}
export declare enum KeyEventType {
    Press = "PRESS",
    Release = "RELEASE"
}
export interface MousePresenceEvent {
    type: MousePresenceEventType;
}
export declare enum MousePresenceEventType {
    Enter = "ENTER",
    Leave = "LEAVE",
    Out = "OUT"
}
export interface WheelEvent {
    deltaY: number;
}
export declare type DiscreteMouseEventHandler = (event: ClickEvent, layer: CanvasWidgetLayer<any, any>) => void;
export declare type DragHandler = (layer: CanvasWidgetLayer<any, any>, dragEvent: CanvasDragEvent) => void;
export declare type KeyboardEventHandler = (event: KeyboardEvent, layer: CanvasWidgetLayer<any, any>) => boolean;
export declare type MousePresenceEventHandler = (event: MousePresenceEvent, layer: CanvasWidgetLayer<any, any>) => void;
export declare type WheelEventHandler = (event: WheelEvent, layer: CanvasWidgetLayer<any, any>) => void;
export interface EventHandlerSet {
    discreteMouseEventHandlers?: DiscreteMouseEventHandler[];
    dragHandlers?: DragHandler[];
    keyboardEventHandlers?: KeyboardEventHandler[];
    mousePresenceEventHandlers?: MousePresenceEventHandler[];
    wheelEventHandlers?: WheelEventHandler[];
}
export declare const formClickEventFromMouseEvent: (e: React.MouseEvent<HTMLCanvasElement, MouseEvent>, t: ClickEventType, i?: TransformationMatrix | undefined) => ClickEvent;
export declare const formWheelEvent: (e: React.WheelEvent<HTMLCanvasElement>) => WheelEvent;
export declare const formKeyboardEvent: (type: KeyEventType, e: React.KeyboardEvent<HTMLDivElement>) => KeyboardEvent;
export declare class CanvasWidgetLayer<LayerProps extends BaseLayerProps, State extends object> {
    _onPaint: OnPaint<LayerProps, State>;
    _onPropsChange: OnPropsChange<LayerProps>;
    _runningOnPropsChange: boolean;
    _props: LayerProps | null;
    _state: State;
    _pixelWidth: number | null;
    _pixelHeight: number | null;
    _canvasElement: HTMLCanvasElement | null;
    _transformMatrix: TransformationMatrix;
    _inverseMatrix: TransformationMatrix;
    _repaintScheduled: boolean;
    _lastRepaintTimestamp: number;
    _discreteMouseEventHandlers: DiscreteMouseEventHandler[];
    _dragHandlers: DragHandler[];
    _keyboardEventHandlers: KeyboardEventHandler[];
    _mousePresenceEventHandlers: MousePresenceEventHandler[];
    _wheelEventHandlers: WheelEventHandler[];
    _refreshRate: number;
    constructor(onPaint: OnPaint<LayerProps, State>, onPropsChange: OnPropsChange<LayerProps>, initialState: State, handlers?: EventHandlerSet);
    getProps(): LayerProps;
    setProps(p: LayerProps): void;
    getState(): State;
    setState(s: State): void;
    getTransformMatrix(): TransformationMatrix;
    setTransformMatrix(t: TransformationMatrix): void;
    pixelWidth(): number;
    pixelHeight(): number;
    resetCanvasElement(canvasElement: any): void;
    canvasElement(): HTMLCanvasElement | null;
    refreshRate(): number;
    setRefreshRate(hz: number): void;
    scheduleRepaint(): void;
    repaintImmediate(): void;
    _doRepaint(): Promise<void>;
    handleDiscreteEvent(e: React.MouseEvent<HTMLCanvasElement, MouseEvent>, type: ClickEventType): void;
    handleDrag(pixelDragRect: RectangularRegion, released: boolean, shift?: boolean, pixelAnchor?: Vec2, pixelPosition?: Vec2): void;
    handleKeyboardEvent(type: KeyEventType, e: React.KeyboardEvent<HTMLDivElement>): boolean;
    handleMousePresenceEvent(e: React.MouseEvent<HTMLCanvasElement, MouseEvent>, type: MousePresenceEventType): void;
    handleWheelEvent(e: React.WheelEvent<HTMLCanvasElement>): void;
}
export declare const useLayer: <LayerProps extends BaseLayerProps, LayerState extends Object>(createLayer: () => CanvasWidgetLayer<LayerProps, LayerState>, layerProps?: LayerProps | undefined) => CanvasWidgetLayer<LayerProps, LayerState> | null;
export declare const useLayers: (layers: (CanvasWidgetLayer<any, any> | null)[]) => (CanvasWidgetLayer<any, any> | null)[];
export {};
