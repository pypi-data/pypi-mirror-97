/// <reference types="react" />
import { RecordingSelection, RecordingSelectionDispatch } from "../../pluginInterface";
import { Electrode } from "./electrodeGeometryLayer";
interface WidgetProps {
    electrodes: Electrode[];
    selection: RecordingSelection;
    selectionDispatch: RecordingSelectionDispatch;
    width: number;
    height: number;
}
declare const ElectrodeGeometryWidget: (props: WidgetProps) => JSX.Element;
export default ElectrodeGeometryWidget;
