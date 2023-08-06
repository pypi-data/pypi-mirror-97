import { CanvasWidgetLayer, KeyboardEventHandler } from "../../common/CanvasWidget/CanvasWidgetLayer";
import { ElectrodeBox } from './setupElectrodes';
import { LayerProps } from './WaveformWidget';
export declare type WaveformColors = {
    base: string;
};
declare type LayerState = {
    electrodeBoxes: ElectrodeBox[];
};
export declare const handleKeyboardEvent: KeyboardEventHandler;
export declare const createWaveformLayer: () => CanvasWidgetLayer<LayerProps, LayerState>;
export {};
