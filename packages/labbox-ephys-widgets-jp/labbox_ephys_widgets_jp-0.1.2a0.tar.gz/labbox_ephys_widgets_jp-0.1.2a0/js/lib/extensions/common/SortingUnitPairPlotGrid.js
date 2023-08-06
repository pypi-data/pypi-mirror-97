import { Grid } from '@material-ui/core';
import React from 'react';
const SortingUnitPairPlotGrid = ({ sorting, selection, selectionDispatch, unitIds, unitPairComponent }) => {
    return (React.createElement(Grid, { container: true, spacing: 0 }, unitIds.map(unitId1 => (React.createElement(Grid, { container: true, key: unitId1 }, unitIds.map(unitId2 => (React.createElement(Grid, { key: unitId2, item: true },
        React.createElement("div", { className: 'plotWrapperStyle' },
            React.createElement("div", { "data-unit-id1": unitId1, "data-unit-id2": unitId2 },
                React.createElement("div", { className: 'plotUnitLabel' },
                    React.createElement("div", null,
                        "Units ",
                        unitId1,
                        " vs ",
                        unitId2)),
                unitPairComponent(unitId1, unitId2)))))))))));
};
export default SortingUnitPairPlotGrid;
//# sourceMappingURL=SortingUnitPairPlotGrid.js.map