import { CalculationPool } from 'labbox';
import React, { FunctionComponent } from 'react';
import { Sorting } from "../pluginInterface";
import './localStyles.css';
interface Props {
    sorting: Sorting;
    onUnitClicked?: (unitId: number, event: {
        ctrlKey?: boolean;
        shiftKey?: boolean;
    }) => void;
    selections: {
        [key: string]: boolean;
    };
    dataFunctionName: string;
    dataFunctionArgsCallback: any;
    boxSize?: {
        width: number;
        height: number;
    };
    plotComponent: React.FunctionComponent<any>;
    plotComponentArgsCallback: any;
    plotComponentPropsCallback?: any;
    calculationPool: CalculationPool | undefined;
}
declare const PlotGrid: FunctionComponent<Props>;
export default PlotGrid;
