import { HitherInterface } from 'labbox';
import { CanvasPainter } from "../../common/CanvasWidget/CanvasPainter";
import { Recording, Sorting } from "../../pluginInterface";
import { SpikeAmplitudesData } from "./useSpikeAmplitudesData";
declare class SpikeAmplitudesPanel {
    private args;
    _updateHandler: (() => void) | null;
    _timeRange: {
        min: number;
        max: number;
    } | null;
    _calculationScheduled: boolean;
    _calculationError: Error | null;
    _yrange: {
        min: number;
        max: number;
    } | null;
    _globalAmplitudeRange: {
        min: number;
        max: number;
    } | null;
    _includeZero: boolean;
    _amplitudes: number[] | undefined;
    constructor(args: {
        spikeAmplitudesData: SpikeAmplitudesData | null;
        recording: Recording;
        sorting: Sorting;
        unitId: number | number[];
        hither: HitherInterface;
    });
    setTimeRange(timeRange: {
        min: number;
        max: number;
    }): void;
    paint(painter: CanvasPainter, completenessFactor: number): void;
    paintYAxis(painter: CanvasPainter, width: number, height: number): void;
    label(): string;
    amplitudeRange(): {
        min: number;
        max: number;
    } | null;
    setGlobalAmplitudeRange(r: {
        min: number;
        max: number;
    }): void;
    autoYRange(): {
        min: number;
        max: number;
    } | null;
    setYRange(yrange: {
        min: number;
        max: number;
    }): void;
    register(onUpdate: () => void): void;
}
declare class CombinedPanel {
    private panels;
    private labelString;
    constructor(panels: SpikeAmplitudesPanel[], labelString: string);
    setTimeRange(timeRange: {
        min: number;
        max: number;
    }): void;
    paint(painter: CanvasPainter, completenessFactor: number): void;
    paintYAxis(painter: CanvasPainter, width: number, height: number): void;
    label(): string;
    register(onUpdate: () => void): void;
}
export declare const combinePanels: (panels: SpikeAmplitudesPanel[], label: string) => CombinedPanel;
export default SpikeAmplitudesPanel;
