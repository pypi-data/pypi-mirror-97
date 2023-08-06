import { Button, Grid } from '@material-ui/core';
import React, { useCallback, useState } from 'react';
import { isMergeGroupRepresentative } from "../pluginInterface";
import { useSortingInfo } from './useSortingInfo';
const SortingUnitPlotGrid = ({ sorting, selection, selectionDispatch, unitComponent }) => {
    const maxUnitsVisibleIncrement = 60;
    const [maxUnitsVisible, setMaxUnitsVisible] = useState(30);
    const sortingInfo = useSortingInfo(sorting.sortingObject, sorting.recordingObject);
    const visibleUnitIds = selection.visibleUnitIds;
    let unit_ids = (sortingInfo ? sortingInfo.unit_ids : [])
        .filter(uid => ((!visibleUnitIds) || (visibleUnitIds.includes(uid))))
        .filter(uid => ((!selection.applyMerges) || (isMergeGroupRepresentative(uid, sorting.curation))));
    let showExpandButton = false;
    if (unit_ids.length > maxUnitsVisible) {
        unit_ids = unit_ids.slice(0, maxUnitsVisible);
        showExpandButton = true;
    }
    // useCheckForChanges('SortingUnitPlotGrid', {sorting, selection, selectionDispatch, unitComponent})
    const handleUnitClick = useCallback((event) => {
        const unitId = Number(event.currentTarget.dataset.unitId);
        selectionDispatch({ type: 'UnitClicked', unitId, ctrlKey: event.ctrlKey, shiftKey: event.shiftKey });
    }, [selectionDispatch]);
    return (React.createElement(Grid, { container: true },
        unit_ids.map(unitId => {
            var _a;
            return (React.createElement(Grid, { key: unitId, item: true },
                React.createElement("div", { className: 'plotWrapperStyle' },
                    React.createElement("div", { "data-unit-id": unitId, className: ((_a = selection.selectedUnitIds) === null || _a === void 0 ? void 0 : _a.includes(unitId)) ? 'plotSelectedStyle' : 'plotUnselectedStyle', onClick: handleUnitClick },
                        React.createElement("div", { className: 'plotUnitLabel' },
                            React.createElement("div", null,
                                "Unit ",
                                unitId)),
                        unitComponent(unitId)))));
        }),
        showExpandButton && (React.createElement("div", { className: 'plotWrapperStyle' },
            React.createElement("div", { className: 'plotWrapperStyleButton' },
                React.createElement(Button, { onClick: () => { setMaxUnitsVisible(maxUnitsVisible + maxUnitsVisibleIncrement); } }, "Show more units"))))));
};
export default SortingUnitPlotGrid;
//# sourceMappingURL=SortingUnitPlotGrid.js.map