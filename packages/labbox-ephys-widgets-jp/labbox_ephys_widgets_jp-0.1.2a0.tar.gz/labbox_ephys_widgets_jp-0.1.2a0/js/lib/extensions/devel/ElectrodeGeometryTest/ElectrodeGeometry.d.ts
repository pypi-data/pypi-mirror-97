/// <reference types="react" />
import { CanvasWidgetLayer } from '../../common/CanvasWidget/CanvasWidgetLayer';
import { RectangularRegion } from '../../common/CanvasWidget/Geometry';
export declare type Electrode = {
    id: number;
    label: string;
    x: number;
    y: number;
};
export interface ElectrodeGeometryProps {
    electrodes: Electrode[];
}
export interface ElectrodeLayerProps extends ElectrodeGeometryProps {
    width: number;
    height: number;
    scaledCoordinates: RectangularRegion;
    electrodeRadius: number;
}
export declare const setCanvasFromProps: (layer: CanvasWidgetLayer<ElectrodeLayerProps, any>, layerProps: ElectrodeLayerProps) => void;
declare const ElectrodeGeometry: (props: ElectrodeGeometryProps) => JSX.Element;
export default ElectrodeGeometry;
