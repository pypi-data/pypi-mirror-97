import React, { useMemo } from 'react';
import SortingUnitPlotGrid from '../../common/SortingUnitPlotGrid';
import IndividualClusterView from './IndividualClusterView';
const IndividualClustersView = ({ recording, sorting, selection, selectionDispatch }) => {
    const unitComponent = useMemo(() => (unitId) => (React.createElement(IndividualClusterView, Object.assign({}, { recording, sorting, unitId, selection, selectionDispatch }, { width: 180, height: 180 }))), [sorting, recording, selection, selectionDispatch]);
    return (React.createElement(SortingUnitPlotGrid, { sorting: sorting, selection: selection, selectionDispatch: selectionDispatch, unitComponent: unitComponent }));
};
export default IndividualClustersView;
//# sourceMappingURL=IndividualClustersView.js.map