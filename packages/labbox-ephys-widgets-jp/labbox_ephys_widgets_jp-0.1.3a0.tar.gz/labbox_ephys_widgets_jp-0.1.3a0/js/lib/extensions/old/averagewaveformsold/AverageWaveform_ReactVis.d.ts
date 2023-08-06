import { FunctionComponent } from 'react';
interface Props {
    boxSize: {
        width: number;
        height: number;
    };
    plotData: {
        sampling_frequency: number;
        average_waveform: number[] | null;
    };
    argsObject: any;
    title: string;
}
declare const AverageWaveform_rv: FunctionComponent<Props>;
export default AverageWaveform_rv;
