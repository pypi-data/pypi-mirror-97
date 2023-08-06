import { createCalculationPool } from 'labbox';
import React, { useCallback } from 'react';
import PlotGrid from '../../common/PlotGrid';
import AverageWaveform_rv from './AverageWaveform_ReactVis';
const averageWaveformsCalculationPool = createCalculationPool({ maxSimultaneous: 6 });
const AverageWaveformsSortingView = ({ sorting, recording, selection, selectionDispatch }) => {
    const selectedUnitIdsLookup = (selection.selectedUnitIds || []).reduce((m, uid) => { m[uid + ''] = true; return m; }, {});
    const handleUnitClicked = useCallback((unitId, event) => {
        selectionDispatch({
            type: 'UnitClicked',
            unitId,
            ctrlKey: event.ctrlKey,
            shiftKey: event.shiftKey
        });
    }, [selectionDispatch]);
    return (React.createElement(PlotGrid, { sorting: sorting, selections: selectedUnitIdsLookup, onUnitClicked: handleUnitClicked, dataFunctionName: 'createjob_fetch_average_waveform_plot_data', dataFunctionArgsCallback: (unitId) => ({
            sorting_object: sorting.sortingObject,
            recording_object: recording.recordingObject,
            unit_id: unitId
        }), 
        // use default boxSize
        plotComponent: AverageWaveform_rv, plotComponentArgsCallback: (unitId) => ({
            id: 'plot-' + unitId
        }), calculationPool: averageWaveformsCalculationPool }));
};
export default AverageWaveformsSortingView;
//# sourceMappingURL=AverageWaveformsSortingView.js.map