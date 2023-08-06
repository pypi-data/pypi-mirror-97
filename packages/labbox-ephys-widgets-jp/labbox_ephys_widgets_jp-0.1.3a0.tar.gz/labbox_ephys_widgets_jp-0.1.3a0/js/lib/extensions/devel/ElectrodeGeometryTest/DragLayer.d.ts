import { CanvasPainter } from '../../common/CanvasWidget/CanvasPainter';
import { CanvasWidgetLayer, DragHandler } from '../../common/CanvasWidget/CanvasWidgetLayer';
import { RectangularRegion } from '../../common/CanvasWidget/Geometry';
import { Electrode, ElectrodeLayerProps } from './ElectrodeGeometry';
export interface DragLayerState {
    dragRegion: RectangularRegion | null;
    electrodeBoundingBoxes: {
        label: string;
        x: number;
        y: number;
        id: number;
        br: RectangularRegion;
    }[];
    selectedElectrodes: Electrode[];
    draggedElectrodes: Electrode[];
}
export declare const setDragLayerStateFromProps: (layer: CanvasWidgetLayer<ElectrodeLayerProps, DragLayerState>, layerProps: ElectrodeLayerProps) => void;
export declare const paintDragLayer: (painter: CanvasPainter, props: ElectrodeLayerProps, state: DragLayerState) => void;
export declare const updateDragRegion: DragHandler;
