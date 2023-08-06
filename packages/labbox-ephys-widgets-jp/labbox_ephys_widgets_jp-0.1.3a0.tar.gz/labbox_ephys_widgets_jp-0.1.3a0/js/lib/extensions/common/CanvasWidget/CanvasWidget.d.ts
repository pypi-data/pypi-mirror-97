/// <reference types="react" />
import { CanvasWidgetLayer } from './CanvasWidgetLayer';
interface Props {
    layers: (CanvasWidgetLayer<any, any> | null)[];
    width: number;
    height: number;
    preventDefaultWheel?: boolean;
}
declare const CanvasWidget: (props: Props) => JSX.Element;
export default CanvasWidget;
