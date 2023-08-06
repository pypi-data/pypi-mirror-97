import { createCalculationPool } from 'labbox';
import React, { useCallback } from 'react';
import PlotGrid from '../../common/PlotGrid';
import AverageWaveformPlotNew from './AverageWaveformPlotNew';
const averageWaveformsCalculationPool = createCalculationPool({ maxSimultaneous: 6 });
const AverageWaveformsNew = (props) => {
    const { selection, selectionDispatch } = props;
    // const { hither } = props
    // const [calcMode, setCalcMode] = useState('waiting')
    // const [result, setResult] = useState<any>(null)
    // useEffect(() => {
    //     if (calcMode === 'waiting') {
    //         setCalcMode('running')
    //         hither.createHitherJob('createjob_test_func_1', {}, {}).wait().then(r => {
    //             setResult(r)
    //             setCalcMode('finished')
    //         })
    //     }
    // }, [hither, setResult, calcMode, setCalcMode])
    // return <div>AAAA: {calcMode} {result + ''}</div>
    const selectedUnitIdsLookup = (selection.selectedUnitIds || []).reduce((m, uid) => { m[uid + ''] = true; return m; }, {});
    const handleUnitClicked = useCallback((unitId, event) => {
        selectionDispatch({
            type: 'UnitClicked',
            unitId,
            ctrlKey: event.ctrlKey,
            shiftKey: event.shiftKey
        });
    }, [selectionDispatch]);
    return (React.createElement(PlotGrid, { sorting: props.sorting, selections: selectedUnitIdsLookup, onUnitClicked: handleUnitClicked, dataFunctionName: 'createjob_fetch_average_waveform_plot_data', dataFunctionArgsCallback: (unitId) => ({
            sorting_object: props.sorting.sortingObject,
            recording_object: props.recording.recordingObject,
            unit_id: unitId
        }), 
        // use default boxSize
        plotComponent: AverageWaveformPlotNew, plotComponentArgsCallback: (unitId) => ({
            id: 'plot-' + unitId
        }), calculationPool: averageWaveformsCalculationPool }));
};
export default AverageWaveformsNew;
//# sourceMappingURL=AverageWaveformsNew.js.map