import { FunctionComponent } from 'react';
export interface SpanWidgetInfo {
    numTimepoints: number | null;
    currentTime?: number | null;
    timeRange?: {
        min: number;
        max: number;
    } | null;
}
interface Props {
    width: number;
    height: number;
    info: SpanWidgetInfo;
    onCurrentTimeChanged: (t: number | null) => void;
    onTimeRangeChanged: (tr: {
        min: number;
        max: number;
    }) => void;
}
declare const TimeSpanWidget: FunctionComponent<Props>;
export default TimeSpanWidget;
