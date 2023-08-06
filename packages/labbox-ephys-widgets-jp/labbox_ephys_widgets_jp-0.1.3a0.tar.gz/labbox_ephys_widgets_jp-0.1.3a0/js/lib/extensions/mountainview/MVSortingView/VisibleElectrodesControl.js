import { Button, Radio } from '@material-ui/core';
import React, { useCallback, useEffect, useMemo, useState } from 'react';
const VisibleElectrodesControl = ({ recordingInfo, selection, selectionDispatch }) => {
    const [mode, setMode] = useState('all');
    const [customElectrodeIds, setCustomElectrodeIds] = useState([]);
    const { selectedElectrodeIds } = selection;
    const handleModeAll = useCallback(() => {
        setMode('all');
    }, [setMode]);
    const handleModeCustom = useCallback(() => {
        setMode('custom');
    }, [setMode]);
    useEffect(() => {
        const includeElectrode = (eid) => {
            switch (mode) {
                case 'all': return true;
                case 'custom': return customElectrodeIds.includes(eid);
                default: throw Error('Unexpected mode');
            }
        };
        const visibleElectrodeIds = ((recordingInfo === null || recordingInfo === void 0 ? void 0 : recordingInfo.channel_ids) || []).filter(eid => includeElectrode(eid));
        selectionDispatch({ type: 'SetVisibleElectrodeIds', visibleElectrodeIds });
    }, [recordingInfo, selectionDispatch, mode, customElectrodeIds]);
    const handleRestrictToSelected = useCallback(() => {
        setMode('custom');
        setCustomElectrodeIds(selectedElectrodeIds || []);
    }, [selectedElectrodeIds, setMode, setCustomElectrodeIds]);
    const hasSelection = useMemo(() => ((selectedElectrodeIds || []).length > 0), [selectedElectrodeIds]);
    return (React.createElement("div", null,
        React.createElement("span", { style: { whiteSpace: 'nowrap' } },
            React.createElement(Radio, { checked: mode === 'all', onClick: handleModeAll }),
            " Show all"),
        React.createElement("span", { style: { whiteSpace: 'nowrap' } },
            React.createElement(Radio, { checked: mode === 'custom', onClick: handleModeCustom }),
            " Show custom"),
        React.createElement(Button, { disabled: !hasSelection, onClick: handleRestrictToSelected }, "Restrict to selected")));
};
export default VisibleElectrodesControl;
//# sourceMappingURL=VisibleElectrodesControl.js.map