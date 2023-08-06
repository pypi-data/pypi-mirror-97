import { Button, Grid } from '@material-ui/core';
import { createCalculationPool } from 'labbox';
import React, { useState } from 'react';
import sizeMe from 'react-sizeme';
import { useSortingInfo } from '../../common/useSortingInfo';
import IndividualUnit from './IndividualUnit';
const individualUnitsCalculationPool = createCalculationPool({ maxSimultaneous: 6 });
const IndividualUnits = ({ size, sorting, recording, selection }) => {
    const maxUnitsVisibleIncrement = 4;
    const [maxUnitsVisible, setMaxUnitsVisible] = useState(4);
    // const { workspaceName, feedUri, readOnly } = workspaceInfo || {};
    const sortingInfo = useSortingInfo(sorting.sortingObject, sorting.recordingObject);
    if (!sortingInfo)
        return React.createElement("div", null, "No sorting info");
    let selectedUnitIdsArray = selection.selectedUnitIds || [];
    let showExpandButton = false;
    if (selectedUnitIdsArray.length > maxUnitsVisible) {
        selectedUnitIdsArray = selectedUnitIdsArray.slice(0, maxUnitsVisible);
        showExpandButton = true;
    }
    // const computeLayout = (marginInPx, maxSize = 800) => {
    //     // we need to fit a square of side length n elements into the wrapper's width.
    //     if (n < 1) return;
    //     // note adjacent margins will collapse, and we don't care about vertical length
    //     // (the user can scroll). So: horizontal space taken is:
    //     // width = n*plotWidth + 2*margin (2 outer margins) + (n-1)*margin (gutters between plots)
    //     // width = margin*(n+1) + plotWidth * n
    //     // Solve for plotWidth = (width - margin*(n+1))/n.
    //     // And we can't have fractional pixels, so round down.
    //     const plotWidth = Math.min(maxSize, Math.floor((size.width - marginInPx*(n + 1))/n));
    //     return plotWidth;
    // }
    const width = size.width;
    if (!width)
        return React.createElement("div", null, "No width");
    return (React.createElement(Grid, { container: true, direction: "column" },
        selectedUnitIdsArray.map(id => (React.createElement(Grid, { item: true, key: id },
            React.createElement("h3", null,
                "Unit ",
                id),
            React.createElement(IndividualUnit, { sorting: sorting, recording: recording, unitId: id, calculationPool: individualUnitsCalculationPool, width: width, sortingInfo: sortingInfo })))),
        showExpandButton ? (React.createElement(Grid, { item: true, key: "expand" },
            React.createElement(Button, { onClick: () => { setMaxUnitsVisible(maxUnitsVisible + maxUnitsVisibleIncrement); } }, "Show more selected units"))) : ((selectedUnitIdsArray.length === 0) &&
            React.createElement("div", null, "Select one or more units"))));
};
export default sizeMe()(IndividualUnits);
//# sourceMappingURL=IndividualUnits.js.map