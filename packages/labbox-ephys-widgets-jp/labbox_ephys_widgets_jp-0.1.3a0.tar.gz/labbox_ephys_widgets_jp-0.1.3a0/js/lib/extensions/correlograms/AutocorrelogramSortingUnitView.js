import React from 'react';
import ClientSidePlot from '../common/ClientSidePlot';
import Correlogram_rv from './Correlogram_ReactVis';
const AutocorrelogramSortingUnitView = ({ sorting, unitId, calculationPool }) => {
    return (React.createElement(ClientSidePlot, { dataFunctionName: "createjob_fetch_correlogram_plot_data", dataFunctionArgs: {
            sorting_object: sorting.sortingObject,
            unit_x: unitId
        }, boxSize: {
            width: 300,
            height: 300
        }, title: "Autocorrelogram", PlotComponent: Correlogram_rv, plotComponentArgs: { id: unitId }, calculationPool: calculationPool }));
};
export default AutocorrelogramSortingUnitView;
//# sourceMappingURL=AutocorrelogramSortingUnitView.js.map