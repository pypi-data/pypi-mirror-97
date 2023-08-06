import { CalculationPool } from 'labbox';
import { FunctionComponent } from 'react';
import { Recording, Sorting, SortingInfo } from "../../pluginInterface";
interface Props {
    sorting: Sorting;
    recording: Recording;
    unitId: number;
    width: number;
    calculationPool: CalculationPool;
    sortingInfo: SortingInfo;
}
declare const IndividualUnit: FunctionComponent<Props>;
export default IndividualUnit;
