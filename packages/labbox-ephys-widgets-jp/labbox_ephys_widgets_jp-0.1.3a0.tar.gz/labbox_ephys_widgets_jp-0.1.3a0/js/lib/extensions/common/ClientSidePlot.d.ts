import { CalculationPool } from 'labbox';
import React, { FunctionComponent } from 'react';
declare const ClientSidePlot: FunctionComponent<{
    dataFunctionName: string;
    dataFunctionArgs: {
        [key: string]: any;
    };
    calculationPool?: CalculationPool;
    boxSize: {
        width: number;
        height: number;
    };
    PlotComponent: React.FunctionComponent<{
        boxSize: {
            width: number;
            height: number;
        };
        plotData: any;
        argsObject: {
            [key: string]: any;
        };
        title: string;
    }>;
    plotComponentArgs: {
        [key: string]: any;
    };
    plotComponentProps?: {
        [key: string]: any;
    };
    title: string;
}>;
export default ClientSidePlot;
