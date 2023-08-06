import React from 'react';
import SpikeAmplitudesTimeWidget from './SpikeAmplitudesTimeWidget';
import useSpikeAmplitudesData from './useSpikeAmplitudesData';
const SpikeAmplitudesUnitView = (props) => {
    const spikeAmplitudesData = useSpikeAmplitudesData(props.recording.recordingObject, props.sorting.sortingObject);
    if (!spikeAmplitudesData) {
        return React.createElement("div", null, "Creating spike amplitudes data...");
    }
    return (React.createElement(SpikeAmplitudesTimeWidget, Object.assign({ spikeAmplitudesData: spikeAmplitudesData, recording: props.recording, sorting: props.sorting, unitIds: [props.unitId] }, { width: props.width || 500, height: props.height || 500 }, { selection: props.selection, selectionDispatch: props.selectionDispatch })));
};
export default SpikeAmplitudesUnitView;
//# sourceMappingURL=SpikeAmplitudesUnitView.js.map