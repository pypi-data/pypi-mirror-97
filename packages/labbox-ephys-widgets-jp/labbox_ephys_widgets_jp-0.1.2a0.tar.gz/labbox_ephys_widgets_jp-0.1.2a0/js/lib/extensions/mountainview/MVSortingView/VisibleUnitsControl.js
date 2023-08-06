import { Checkbox } from '@material-ui/core';
import { useHitherJob } from 'labbox';
import React, { useCallback, useEffect, useState } from 'react';
import { useSortingInfo } from '../../common/useSortingInfo';
const VisibleUnitsControl = ({ sorting, recording, selection, selectionDispatch }) => {
    const sortingInfo = useSortingInfo(sorting.sortingObject, sorting.recordingObject);
    const [hideRejected, setHideRejected] = useState(false);
    const [showAcceptedOnly, setShowAcceptedOnly] = useState(false);
    const [restrictToVisibleElectrodes, setRestrictToVisibleElectrodes] = useState(true);
    const visibleElectrodeIds = selection.visibleElectrodeIds;
    const { result: peakElectrodeIds } = useHitherJob('createjob_get_peak_channels', { sorting_object: sorting.sortingObject, recording_object: recording.recordingObject }, { useClientCache: true });
    const handleShowAcceptedOnly = useCallback(() => {
        setShowAcceptedOnly(!showAcceptedOnly);
    }, [showAcceptedOnly]);
    const handleHideRejected = useCallback(() => {
        setHideRejected(!hideRejected);
    }, [hideRejected]);
    const handleRestrictToVisibleElectrodes = useCallback(() => {
        setRestrictToVisibleElectrodes(!restrictToVisibleElectrodes);
    }, [restrictToVisibleElectrodes]);
    useEffect(() => {
        const includeUnit = (uid) => {
            if ((restrictToVisibleElectrodes) && (visibleElectrodeIds) && (peakElectrodeIds)) {
                const peakElectrodeId = peakElectrodeIds[uid + ''];
                if (!visibleElectrodeIds.includes(peakElectrodeId))
                    return false;
            }
            if (showAcceptedOnly) {
                return getLabelsForUnitId(uid, sorting).includes('accept');
            }
            else if (hideRejected) {
                return !getLabelsForUnitId(uid, sorting).includes('reject');
            }
            else {
                return true;
            }
        };
        const visibleUnitIds = ((sortingInfo === null || sortingInfo === void 0 ? void 0 : sortingInfo.unit_ids) || []).filter(uid => includeUnit(uid));
        selectionDispatch({ type: 'SetVisibleUnitIds', visibleUnitIds });
    }, [sorting, selectionDispatch, sortingInfo, showAcceptedOnly, hideRejected, restrictToVisibleElectrodes, visibleElectrodeIds, peakElectrodeIds]);
    return (React.createElement("div", null,
        React.createElement("span", { style: { whiteSpace: 'nowrap' } },
            React.createElement(Checkbox, { checked: showAcceptedOnly, onClick: handleShowAcceptedOnly }),
            " Show accepted only"),
        React.createElement("span", { style: { whiteSpace: 'nowrap' } },
            React.createElement(Checkbox, { checked: hideRejected, onClick: handleHideRejected, disabled: showAcceptedOnly }),
            " Hide rejected"),
        React.createElement("span", { style: { whiteSpace: 'nowrap' } },
            React.createElement(Checkbox, { checked: restrictToVisibleElectrodes, onClick: handleRestrictToVisibleElectrodes, disabled: !visibleElectrodeIds }),
            " Restrict to visible electrodes")));
};
const getLabelsForUnitId = (unitId, sorting) => {
    const labelsByUnit = (sorting.curation || {}).labelsByUnit || {};
    return labelsByUnit[unitId] || [];
};
export default VisibleUnitsControl;
//# sourceMappingURL=VisibleUnitsControl.js.map