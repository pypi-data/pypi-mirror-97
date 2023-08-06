import { CanvasWidgetLayer } from "../../common/CanvasWidget/CanvasWidgetLayer";
import { RectangularRegion } from "../../common/CanvasWidget/Geometry";
export declare type ClusterLayerProps = {
    x: number[];
    y: number[];
    rect: RectangularRegion;
    width: number;
    height: number;
    selectedIndex?: number;
    onSelectedIndexChanged?: (i: number | undefined) => void;
};
declare type ClusterLayerState = {
    hoverIndex?: number;
};
declare const createClusterLayer: () => CanvasWidgetLayer<ClusterLayerProps, ClusterLayerState>;
export default createClusterLayer;
