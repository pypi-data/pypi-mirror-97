import { HitherContext } from 'labbox';
import React, { useContext, useEffect, useMemo, useState } from 'react';
import useBufferedDispatch from '../../common/useBufferedDispatch';
import { useRecordingInfo } from '../../common/useRecordingInfo';
import { useSortingInfo } from '../../common/useSortingInfo';
import { getArrayMax, getArrayMin } from '../../common/Utility';
import { applyMergesToUnit, sortingSelectionReducer } from "../../pluginInterface";
import TimeWidgetNew from '../../timeseries/TimeWidgetNew/TimeWidgetNew';
import SpikeAmplitudesPanel, { combinePanels } from './SpikeAmplitudesPanel';
const SpikeAmplitudesTimeWidget = ({ spikeAmplitudesData, recording, sorting, unitIds, width, height, selection: externalSelection, selectionDispatch: externalSelectionDispatch }) => {
    const hither = useContext(HitherContext);
    const sortingInfo = useSortingInfo(sorting.sortingObject, sorting.recordingObject);
    const recordingInfo = useRecordingInfo(recording.recordingObject);
    const [selection, selectionDispatch] = useBufferedDispatch(sortingSelectionReducer, externalSelection, useMemo(() => ((state) => { externalSelectionDispatch({ type: 'Set', state }); }), [externalSelectionDispatch]), 400);
    const [spikeAmplitudesPanels, setSpikeAmplitudesPanels] = useState(null);
    useEffect(() => {
        const panels = [];
        const allMins = [];
        const allMaxs = [];
        unitIds.forEach(unitId => {
            const uid = applyMergesToUnit(unitId, sorting.curation, selection.applyMerges);
            const p = new SpikeAmplitudesPanel({ spikeAmplitudesData, recording, sorting, unitId: uid, hither });
            const amps = spikeAmplitudesData.getSpikeAmplitudes(uid);
            if (amps) {
                allMins.push(amps.minAmp);
                allMaxs.push(amps.maxAmp);
            }
            panels.push(p);
        });
        // we want the y-axis to show even when no units are selected
        if (panels.length === 0) {
            panels.push(new SpikeAmplitudesPanel({
                spikeAmplitudesData: null,
                recording,
                sorting,
                unitId: -1,
                hither
            }));
        }
        if (allMins.length > 0) {
            panels.forEach(p => {
                p.setGlobalAmplitudeRange({ min: getArrayMin(allMins), max: getArrayMax(allMaxs) });
            });
        }
        setSpikeAmplitudesPanels(panels);
    }, [unitIds, sorting, hither, recording, spikeAmplitudesData, selection]); // important that this depends on selection so that we refresh when time range changes
    const panels = useMemo(() => (spikeAmplitudesPanels ? [combinePanels(spikeAmplitudesPanels, '')] : []), [spikeAmplitudesPanels]);
    if (!sortingInfo)
        return React.createElement("div", null, "No sorting info");
    if (!recordingInfo)
        return React.createElement("div", null, "No recording info");
    return (React.createElement(TimeWidgetNew, { panels: panels, width: width, height: height, samplerate: sortingInfo.samplerate, maxTimeSpan: sortingInfo.samplerate * 60 * 5, startTimeSpan: sortingInfo.samplerate * 60 * 1, numTimepoints: recordingInfo.num_frames, selection: selection, selectionDispatch: selectionDispatch }));
};
export default SpikeAmplitudesTimeWidget;
//# sourceMappingURL=SpikeAmplitudesTimeWidget.js.map