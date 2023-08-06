import { createCalculationPool, useHitherJob } from 'labbox';
import React from 'react';
import { VerticalBarSeries, XAxis, XYPlot, YAxis } from 'react-vis';
import HitherJobStatusView from '../common/HitherJobStatusView';
import { applyMergesToUnit } from "../pluginInterface";
const calculationPool = createCalculationPool({ maxSimultaneous: 6 });
const Correlogram_rv2 = ({ sorting, unitId1, unitId2, selection, selectionDispatch, width, height }) => {
    const { result: plotData, job } = useHitherJob('createjob_fetch_correlogram_plot_data', {
        sorting_object: sorting.sortingObject,
        unit_x: applyMergesToUnit(unitId1, sorting.curation, selection.applyMerges),
        unit_y: unitId2 !== undefined ? applyMergesToUnit(unitId2, sorting.curation, selection.applyMerges) : null
    }, { useClientCache: false, calculationPool });
    if (!plotData) {
        return React.createElement(HitherJobStatusView, { job: job, width: width, height: height });
    }
    const data = plotData.bins.map((item, index) => {
        return { x: item, y: plotData.bin_counts[index] };
    });
    const xAxisLabel = 'dt (msec)';
    return (React.createElement("div", { className: "App" },
        React.createElement(XYPlot, { margin: 30, height: height, width: width },
            React.createElement(VerticalBarSeries, { data: data, barWidth: 1 }),
            React.createElement(XAxis, null),
            React.createElement(YAxis, null)),
        React.createElement("div", { style: { textAlign: 'center', fontSize: '12px' } }, xAxisLabel)));
};
export default Correlogram_rv2;
//# sourceMappingURL=Correlogram_ReactVis2.js.map