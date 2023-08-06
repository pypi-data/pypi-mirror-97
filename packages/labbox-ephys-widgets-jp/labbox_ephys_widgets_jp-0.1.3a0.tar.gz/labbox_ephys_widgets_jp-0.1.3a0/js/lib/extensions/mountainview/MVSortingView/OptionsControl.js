import { Checkbox } from '@material-ui/core';
import React, { useCallback } from 'react';
const OptionsControl = ({ selection, selectionDispatch }) => {
    return (React.createElement("div", null,
        React.createElement(WaveformLayoutControl, { selection: selection, selectionDispatch: selectionDispatch })));
};
const WaveformLayoutControl = ({ selection, selectionDispatch }) => {
    const waveformsMode = selection.waveformsMode || 'geom';
    const checked = waveformsMode === 'geom';
    const handleToggle = useCallback(() => {
        selectionDispatch({ type: 'SetWaveformsMode', waveformsMode: waveformsMode === 'geom' ? 'vertical' : 'geom' });
    }, [waveformsMode, selectionDispatch]);
    return (React.createElement("div", null,
        React.createElement("span", null, "Waveforms:"),
        React.createElement("span", { style: { whiteSpace: 'nowrap' } },
            React.createElement(Checkbox, { checked: checked, onClick: handleToggle }),
            " Use electrode geom")));
};
export default OptionsControl;
//# sourceMappingURL=OptionsControl.js.map