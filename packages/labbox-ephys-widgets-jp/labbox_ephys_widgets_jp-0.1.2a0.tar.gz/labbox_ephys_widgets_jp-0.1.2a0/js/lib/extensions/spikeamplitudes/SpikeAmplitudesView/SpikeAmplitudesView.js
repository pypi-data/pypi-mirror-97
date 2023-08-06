import React from 'react';
import Splitter from '../../common/Splitter';
import SelectUnitsWidget from './SelectUnitsWidget';
import SpikeAmplitudesTimeWidget from './SpikeAmplitudesTimeWidget';
import useSpikeAmplitudesData from './useSpikeAmplitudesData';
const SpikeAmplitudesView = ({ recording, sorting, selection, selectionDispatch, width, height }) => {
    const spikeAmplitudesData = useSpikeAmplitudesData(recording.recordingObject, sorting.sortingObject);
    if (!spikeAmplitudesData) {
        return React.createElement("div", null, "Creating spike amplitudes data...");
    }
    return (React.createElement(Splitter, { width: width || 600, height: height || 900, initialPosition: 200 },
        React.createElement(SelectUnitsWidget, { sorting: sorting, selection: selection, selectionDispatch: selectionDispatch }),
        React.createElement(SpikeAmplitudesTimeWidget, Object.assign({ spikeAmplitudesData: spikeAmplitudesData, recording: recording, sorting: sorting, unitIds: selection.selectedUnitIds || [] }, { width: 0, height: 0 }, { selection: selection, selectionDispatch: selectionDispatch }))));
};
export default SpikeAmplitudesView;
//# sourceMappingURL=SpikeAmplitudesView.js.map