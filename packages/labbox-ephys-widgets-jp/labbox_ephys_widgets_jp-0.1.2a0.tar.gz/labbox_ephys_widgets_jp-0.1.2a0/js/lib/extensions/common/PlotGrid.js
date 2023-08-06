import { Button, Grid } from '@material-ui/core';
import React, { useState } from 'react';
import ClientSidePlot from './ClientSidePlot';
import './localStyles.css';
import { useSortingInfo } from './useSortingInfo';
const isSelected = (query, selections = {}) => (selections[query] ? true : false);
const PlotGrid = ({ sorting, onUnitClicked, selections, dataFunctionName, dataFunctionArgsCallback, // fix this
boxSize = { width: 200, height: 200 }, plotComponent, plotComponentArgsCallback, plotComponentPropsCallback, // fix this
calculationPool = undefined }) => {
    const maxUnitsVisibleIncrement = 60;
    const [maxUnitsVisible, setMaxUnitsVisible] = useState(30);
    const sortingInfo = useSortingInfo(sorting.sortingObject, sorting.recordingObject);
    let unit_ids = sortingInfo ? sortingInfo.unit_ids : [];
    let showExpandButton = false;
    if (unit_ids.length > maxUnitsVisible) {
        unit_ids = unit_ids.slice(0, maxUnitsVisible);
        showExpandButton = true;
    }
    return (React.createElement(Grid, { container: true },
        unit_ids.map(unitId => (React.createElement(Grid, { key: unitId, item: true },
            React.createElement("div", { className: 'plotWrapperStyle' },
                React.createElement("div", { className: isSelected(unitId + '', selections) ? 'plotSelectedStyle' : 'plotUnselectedStyle', onClick: (event) => { onUnitClicked && onUnitClicked(unitId, event); } },
                    React.createElement("div", { className: 'plotUnitLabel' },
                        React.createElement("div", null,
                            "Unit ",
                            unitId)),
                    React.createElement(ClientSidePlot, { dataFunctionName: dataFunctionName, dataFunctionArgs: dataFunctionArgsCallback(unitId), boxSize: boxSize, PlotComponent: plotComponent, plotComponentArgs: plotComponentArgsCallback(unitId), plotComponentProps: plotComponentPropsCallback ? plotComponentPropsCallback(unitId) : undefined, calculationPool: calculationPool, title: "" })))))),
        showExpandButton && (React.createElement("div", { className: 'plotWrapperStyle' },
            React.createElement("div", { className: 'plotWrapperStyleButton' },
                React.createElement(Button, { onClick: () => { setMaxUnitsVisible(maxUnitsVisible + maxUnitsVisibleIncrement); } }, "Show more units"))))));
};
export default PlotGrid;
//# sourceMappingURL=PlotGrid.js.map