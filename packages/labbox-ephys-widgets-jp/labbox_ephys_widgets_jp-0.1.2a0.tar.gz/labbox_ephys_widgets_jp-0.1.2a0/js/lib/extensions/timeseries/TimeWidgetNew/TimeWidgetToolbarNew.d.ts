import { FunctionComponent } from 'react';
interface Props {
    width: number;
    height: number;
    top: number;
    onZoomIn: () => void;
    onZoomOut: () => void;
    onShiftTimeLeft: () => void;
    onShiftTimeRight: () => void;
    customActions?: any[] | null;
}
declare const TimeWidgetToolbarNew: FunctionComponent<Props>;
export default TimeWidgetToolbarNew;
