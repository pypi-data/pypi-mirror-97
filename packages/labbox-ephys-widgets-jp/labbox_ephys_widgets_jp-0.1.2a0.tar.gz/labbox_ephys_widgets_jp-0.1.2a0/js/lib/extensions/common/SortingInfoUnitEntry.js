import React from 'react';
import './localStyles.css';
const SortingInfoUnitEntry = ({ unitId, labels = "", unitStatus = 'unselected', onUnitClicked }) => {
    const unitClass = unitStatus === 'selected' ? 'selectedUnitEntry' : 'unselectedUnitEntry'; // default to unselected
    return (React.createElement("div", { className: unitClass, onClick: (event) => onUnitClicked(unitId, event) },
        React.createElement("span", { className: 'unitEntryBase' }, unitId),
        React.createElement("span", { className: 'unitLabelsStyle' }, labels)));
};
export default SortingInfoUnitEntry;
//# sourceMappingURL=SortingInfoUnitEntry.js.map