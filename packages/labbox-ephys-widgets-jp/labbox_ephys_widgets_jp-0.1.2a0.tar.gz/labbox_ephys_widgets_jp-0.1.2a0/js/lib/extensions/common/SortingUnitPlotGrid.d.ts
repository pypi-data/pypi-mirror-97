import React, { FunctionComponent } from 'react';
import { Sorting, SortingSelection, SortingSelectionDispatch } from "../pluginInterface";
declare type Props = {
    sorting: Sorting;
    selection: SortingSelection;
    selectionDispatch: SortingSelectionDispatch;
    unitComponent: (unitId: number) => React.ReactElement;
};
declare const SortingUnitPlotGrid: FunctionComponent<Props>;
export default SortingUnitPlotGrid;
