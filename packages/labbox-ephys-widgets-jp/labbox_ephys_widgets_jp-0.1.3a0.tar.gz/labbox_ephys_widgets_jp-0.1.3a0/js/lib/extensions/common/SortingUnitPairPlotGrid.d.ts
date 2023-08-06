import React, { FunctionComponent } from 'react';
import { Sorting, SortingSelection, SortingSelectionDispatch } from "../pluginInterface";
declare type Props = {
    sorting: Sorting;
    selection: SortingSelection;
    selectionDispatch: SortingSelectionDispatch;
    unitIds: number[];
    unitPairComponent: (unitId1: number, unitId2: number) => React.ReactElement;
};
declare const SortingUnitPairPlotGrid: FunctionComponent<Props>;
export default SortingUnitPairPlotGrid;
