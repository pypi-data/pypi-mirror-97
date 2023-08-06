/// <reference types="react" />
import { CanvasPainter } from '../../common/CanvasWidget/CanvasPainter';
import { ActionItem, DividerItem } from '../../common/Toolbars';
import { RecordingSelection, RecordingSelectionDispatch } from "../../pluginInterface";
export declare type TimeWidgetAction = ActionItem | DividerItem;
interface Props {
    panels: TimeWidgetPanel[];
    customActions?: TimeWidgetAction[] | null;
    width: number;
    height: number;
    samplerate: number;
    maxTimeSpan: number;
    startTimeSpan: number;
    numTimepoints: number;
    selection: RecordingSelection;
    selectionDispatch: RecordingSelectionDispatch;
}
export interface TimeWidgetPanel {
    setTimeRange: (timeRange: {
        min: number;
        max: number;
    }) => void;
    paint: (painter: CanvasPainter, completenessFactor: number) => void;
    paintYAxis?: (painter: CanvasPainter, width: number, height: number) => void;
    label: () => string;
}
declare const TimeWidgetNew: (props: Props) => JSX.Element;
export default TimeWidgetNew;
