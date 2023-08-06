import React, { useMemo } from 'react';
import SortingUnitPlotGrid from '../common/SortingUnitPlotGrid';
import CorrelogramRv2 from './Correlogram_ReactVis2';
// const autocorrelogramsCalculationPool = createCalculationPool({maxSimultaneous: 6});
const AutoCorrelograms = ({ sorting, selection, selectionDispatch }) => {
    const unitComponent = useMemo(() => (unitId) => (React.createElement(CorrelogramRv2, Object.assign({}, { sorting, unitId1: unitId, selection, selectionDispatch }, { width: 180, height: 180 }))), [sorting, selection, selectionDispatch]);
    return (React.createElement(SortingUnitPlotGrid, { sorting: sorting, selection: selection, selectionDispatch: selectionDispatch, unitComponent: unitComponent }));
    // return (
    //     <PlotGrid
    //         sorting={sorting}
    //         selections={selectedUnitIdsLookup}
    //         onUnitClicked={handleUnitClicked}
    //         dataFunctionName={'createjob_fetch_correlogram_plot_data'}
    //         dataFunctionArgsCallback={(unitId: number) => ({
    //             sorting_object: sorting.sortingObject,
    //             unit_x: unitId
    //         })}
    //         // use default boxSize
    //         plotComponent={Correlogram_rv}
    //         plotComponentArgsCallback={(unitId: number) => ({
    //             id: 'plot-'+unitId
    //         })}
    //         calculationPool={autocorrelogramsCalculationPool}
    //     />
    // );
};
export default AutoCorrelograms;
//# sourceMappingURL=AutoCorrelograms.js.map