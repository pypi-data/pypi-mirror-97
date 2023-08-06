import { FunctionComponent } from 'react';
interface Props {
    boxSize: {
        width: number;
        height: number;
    };
    plotData: any;
    argsObject: any;
    title: string;
}
declare const SpikeWaveforms_rv: FunctionComponent<Props>;
export default SpikeWaveforms_rv;
