import { CalculationPool } from 'labbox';
import { FunctionComponent } from 'react';
import { Sorting } from "../pluginInterface";
declare const AutocorrelogramSortingUnitView: FunctionComponent<{
    sorting: Sorting;
    unitId: number;
    calculationPool: CalculationPool;
}>;
export default AutocorrelogramSortingUnitView;
