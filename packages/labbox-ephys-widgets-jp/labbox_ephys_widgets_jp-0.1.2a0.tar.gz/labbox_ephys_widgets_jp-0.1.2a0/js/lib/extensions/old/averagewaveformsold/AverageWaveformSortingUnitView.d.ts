import { CalculationPool } from 'labbox';
import { FunctionComponent } from 'react';
import { Recording, Sorting } from "../../pluginInterface";
declare const AverageWaveformSortingUnitView: FunctionComponent<{
    sorting: Sorting;
    recording: Recording;
    unitId: number;
    calculationPool: CalculationPool;
}>;
export default AverageWaveformSortingUnitView;
