import { FunctionComponent } from 'react';
interface Props {
    boxSize: {
        width: number;
        height: number;
    };
    plotData: any | null;
    argsObject: any;
    title: string;
}
declare const Correlogram_rv: FunctionComponent<Props>;
export default Correlogram_rv;
