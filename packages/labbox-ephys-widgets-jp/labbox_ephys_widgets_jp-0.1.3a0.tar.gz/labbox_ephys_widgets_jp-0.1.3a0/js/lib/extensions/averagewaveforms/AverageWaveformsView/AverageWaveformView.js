import { createCalculationPool, useHitherJob } from 'labbox';
import React, { useMemo } from 'react';
import HitherJobStatusView from '../../common/HitherJobStatusView';
import { applyMergesToUnit } from "../../pluginInterface";
import WaveformWidget from './WaveformWidget';
const calculationPool = createCalculationPool({ maxSimultaneous: 6 });
const AverageWaveformView = ({ sorting, recording, unitId, selection, selectionDispatch, width, height, noiseLevel, customActions }) => {
    const { result: plotData, job } = useHitherJob('createjob_fetch_average_waveform_2', {
        sorting_object: sorting.sortingObject,
        recording_object: recording.recordingObject,
        unit_id: applyMergesToUnit(unitId, sorting.curation, selection.applyMerges)
    }, { useClientCache: true, calculationPool });
    const electrodeOpts = useMemo(() => ({}), []);
    if (!plotData) {
        return React.createElement(HitherJobStatusView, { job: job, width: width, height: height });
    }
    const visibleElectrodeIds = selection.visibleElectrodeIds;
    const electrodeIds = plotData.channel_ids.filter(id => ((!visibleElectrodeIds) || (visibleElectrodeIds.includes(id))));
    const electrodeLocations = plotData.channel_locations.filter((loc, ii) => ((!visibleElectrodeIds) || (visibleElectrodeIds.includes(plotData.channel_ids[ii]))));
    return (React.createElement(WaveformWidget, { waveform: plotData.average_waveform, layoutMode: selection.waveformsMode || 'geom', noiseLevel: noiseLevel, electrodeIds: electrodeIds, electrodeLocations: electrodeLocations, samplingFrequency: plotData.sampling_frequency, width: width, height: height, selection: selection, customActions: customActions, selectionDispatch: selectionDispatch, electrodeOpts: electrodeOpts }));
};
export default AverageWaveformView;
//# sourceMappingURL=AverageWaveformView.js.map