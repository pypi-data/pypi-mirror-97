import { CanvasWidgetLayer } from "../../common/CanvasWidget/CanvasWidgetLayer";
import { RectangularRegion } from '../../common/CanvasWidget/Geometry';
import { ElectrodeBox } from './setupElectrodes';
export declare type ElectrodeColors = {
    border: string;
    base: string;
    selected: string;
    hover: string;
    selectedHover: string;
    dragged: string;
    draggedSelected: string;
    dragRect: string;
    textLight: string;
    textDark: string;
};
declare type LayerState = {
    electrodeBoxes: ElectrodeBox[];
    radius: number;
    pixelRadius: number;
    dragRegion: RectangularRegion | null;
    draggedElectrodeIds: number[];
    hoveredElectrodeId: number | null;
};
export declare const createElectrodesLayer: () => CanvasWidgetLayer<import("./WaveformWidget").Props, LayerState>;
export {};
