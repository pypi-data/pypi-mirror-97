import React from 'react';
import { useSortingInfo } from '../../common/useSortingInfo';
import { isMergeGroupRepresentative } from "../../pluginInterface";
import UnitsTable from '../../unitstable/Units/UnitsTable';
const SelectUnitsWidget = ({ sorting, selection, selectionDispatch }) => {
    const sortingInfo = useSortingInfo(sorting.sortingObject, sorting.recordingObject);
    if (!sortingInfo)
        return React.createElement("div", null, "No sorting info");
    const unitIds = ((sortingInfo === null || sortingInfo === void 0 ? void 0 : sortingInfo.unit_ids) || [])
        .filter(uid => ((!selection.applyMerges) || (isMergeGroupRepresentative(uid, sorting.curation))));
    return (React.createElement(UnitsTable, Object.assign({ units: unitIds }, { selection, selectionDispatch, sorting })));
};
export default SelectUnitsWidget;
//# sourceMappingURL=SelectUnitsWidget.js.map