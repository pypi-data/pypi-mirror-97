import { CanvasWidgetLayer } from "../../common/CanvasWidget/CanvasWidgetLayer";
import { RectangularRegion } from "../../common/CanvasWidget/Geometry";
interface ElectrodeBoundingBox extends Electrode {
    id: number;
    br: RectangularRegion;
}
export declare type Electrode = {
    id: number;
    label: string;
    x: number;
    y: number;
    color?: string;
};
export interface ElectrodeLayerProps {
    electrodes: Electrode[];
    selectedElectrodeIds: number[];
    onSelectedElectrodeIdsChanged: (x: number[]) => void;
    width: number;
    height: number;
}
interface ElectrodeLayerState {
    electrodeBoundingBoxes: ElectrodeBoundingBox[];
    dragRegion: RectangularRegion | null;
    draggedElectrodeIds: number[];
    hoveredElectrodeId: number | null;
    radius: number;
    pixelRadius: number;
    lastProps: ElectrodeLayerProps;
}
export declare const createElectrodeGeometryLayer: () => CanvasWidgetLayer<ElectrodeLayerProps, ElectrodeLayerState>;
export {};
