import React, { useMemo } from 'react';
import SortingUnitPairPlotGrid from '../../common/SortingUnitPairPlotGrid';
import CorrelogramRv2 from '../Correlogram_ReactVis2';
const CrossCorrelogramsWidget = ({ sorting, selection, selectionDispatch, unitIds, width, height }) => {
    const plotMargin = 10; // in pixels
    const n = unitIds.length || 1;
    const plotWidth = Math.min(220, (width - (plotMargin * (n + 1))) / n);
    const plotHeight = plotWidth;
    const unitPairComponent = useMemo(() => (unitId1, unitId2) => (React.createElement(CorrelogramRv2, { sorting: sorting, selection: selection, selectionDispatch: selectionDispatch, unitId1: unitId1, unitId2: unitId2, width: plotWidth, height: plotHeight })), [sorting, selection, selectionDispatch, plotWidth, plotHeight]);
    return (React.createElement(SortingUnitPairPlotGrid, { sorting: sorting, selection: selection, selectionDispatch: selectionDispatch, unitIds: unitIds, unitPairComponent: unitPairComponent }));
};
export default CrossCorrelogramsWidget;
//# sourceMappingURL=CrossCorrelogramsWidget.js.map