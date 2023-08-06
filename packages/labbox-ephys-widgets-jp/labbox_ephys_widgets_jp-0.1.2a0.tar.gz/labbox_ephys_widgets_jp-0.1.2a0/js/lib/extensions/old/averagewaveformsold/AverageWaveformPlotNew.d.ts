/// <reference types="react" />
interface PlotData {
    average_waveform: number[];
    sampling_frequency: number;
}
interface Props {
    boxSize: {
        width: number;
        height: number;
    };
    plotData: PlotData;
    argsObject: {
        id: string;
    };
    title: string;
}
declare const AverageWaveformPlotNew: (props: Props) => JSX.Element;
export default AverageWaveformPlotNew;
