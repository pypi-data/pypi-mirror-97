import { FunctionComponent } from 'react';
export interface BottomBarInfo {
    currentTime?: number | null;
    samplerate: number;
    timeRange?: {
        min: number;
        max: number;
    } | null;
    statusText: string;
}
interface Props {
    width: number;
    height: number;
    info: BottomBarInfo;
    onCurrentTimeChanged: (t: number | null) => void;
    onTimeRangeChanged: (tr: {
        min: number;
        max: number;
    }) => void;
}
declare const TimeWidgetBottomBar: FunctionComponent<Props>;
export default TimeWidgetBottomBar;
