import { RectangularRegion, TransformationMatrix, Vec2 } from '../../common/CanvasWidget/Geometry';
export declare type ElectrodeBox = {
    label: string;
    id: number;
    x: number;
    y: number;
    rect: RectangularRegion;
    transform: TransformationMatrix;
};
export declare const getElectrodesAspectRatio: (electrodeLocations: Vec2[]) => number;
declare const setupElectrodes: (args: {
    width: number;
    height: number;
    electrodeLocations: Vec2[];
    electrodeIds: number[];
    layoutMode: 'geom' | 'vertical';
    maxElectrodePixelRadius?: number;
}) => {
    electrodeBoxes: ElectrodeBox[];
    transform: TransformationMatrix;
    radius: number;
    pixelRadius: number;
};
export default setupElectrodes;
