import { FunctionComponent } from 'react';
import { ActionItem, DividerItem } from '../../common/Toolbars';
import { RecordingSelection, RecordingSelectionDispatch } from "../../pluginInterface";
import { ElectrodeColors } from './electrodesLayer';
import { WaveformColors } from './waveformLayer';
export declare type Props = {
    waveform?: number[][];
    layoutMode: 'geom' | 'vertical';
    noiseLevel: number;
    electrodeIds: number[];
    electrodeLocations: number[][];
    samplingFrequency: number;
    width: number;
    height: number;
    selection: RecordingSelection;
    selectionDispatch: RecordingSelectionDispatch;
    electrodeOpts: ElectrodeOpts;
    customActions?: (ActionItem | DividerItem)[];
};
export declare type ElectrodeOpts = {
    colors?: ElectrodeColors;
    showLabels?: boolean;
    disableSelection?: boolean;
    maxElectrodePixelRadius?: number;
};
export declare type LayerProps = Props & {
    layoutMode: 'geom' | 'vertical';
    waveformOpts: {
        colors?: WaveformColors;
        waveformWidth: number;
    };
};
export declare type ElectrodeLayerProps = Props;
declare const WaveformWidget: FunctionComponent<Props>;
export default WaveformWidget;
