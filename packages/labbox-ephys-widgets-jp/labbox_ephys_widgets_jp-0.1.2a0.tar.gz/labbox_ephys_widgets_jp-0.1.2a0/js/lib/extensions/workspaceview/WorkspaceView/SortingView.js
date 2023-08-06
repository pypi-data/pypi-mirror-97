import { createCalculationPool, HitherContext, usePlugins } from 'labbox';
import React, { useCallback, useContext, useEffect, useMemo, useReducer, useState } from 'react';
import Hyperlink from '../../common/Hyperlink';
import { useRecordingInfo } from '../../common/useRecordingInfo';
import { useSortingInfo } from '../../common/useSortingInfo';
import { sortingSelectionReducer, sortingViewPlugins } from '../../pluginInterface';
const calculationPool = createCalculationPool({ maxSimultaneous: 6 });
const SortingView = (props) => {
    const hither = useContext(HitherContext);
    const { readOnly, sorting, recording, curationDispatch, onSetExternalUnitMetrics, workspaceRouteDispatch } = props;
    const [externalUnitMetricsStatus, setExternalUnitMetricsStatus] = useState('waiting');
    //const initialSortingSelection: SortingSelection = {currentTimepoint: 1000, animation: {currentTimepointVelocity: 100, lastUpdateTimestamp: Number(new Date())}}
    const initialSortingSelection = {};
    const [selection, selectionDispatch] = useReducer(sortingSelectionReducer, initialSortingSelection);
    const sortingInfo = useSortingInfo(sorting.sortingObject, sorting.recordingObject);
    const recordingInfo = useRecordingInfo(recording.recordingObject);
    const sortingId = sorting.sortingId;
    useEffect(() => {
        if ((!selection.timeRange) && (recordingInfo)) {
            selectionDispatch({ type: 'SetTimeRange', timeRange: { min: 0, max: Math.min(recordingInfo.num_frames, recordingInfo.sampling_frequency / 10) } });
        }
    }, [selection, recordingInfo]);
    useEffect(() => {
        if ((sorting) && (sorting.externalUnitMetricsUri) && (!sorting.externalUnitMetrics) && (externalUnitMetricsStatus === 'waiting')) {
            setExternalUnitMetricsStatus('computing');
            hither.createHitherJob('fetch_external_sorting_unit_metrics', { uri: sorting.externalUnitMetricsUri }, { useClientCache: true }).wait().then((externalUnitMetrics) => {
                onSetExternalUnitMetrics({ sortingId, externalUnitMetrics: externalUnitMetrics });
                setExternalUnitMetricsStatus('finished');
            });
        }
    }, [onSetExternalUnitMetrics, setExternalUnitMetricsStatus, externalUnitMetricsStatus, sorting, sortingId, hither]);
    const W = props.width || 800;
    const H = props.height || 800;
    const footerHeight = 20;
    const footerStyle = useMemo(() => ({
        position: 'absolute',
        left: 0,
        top: H - footerHeight,
        width: W,
        height: footerHeight,
        overflow: 'hidden'
    }), [W, H, footerHeight]);
    const contentWidth = W;
    const contentHeight = H - footerHeight;
    const contentWrapperStyle = useMemo(() => ({
        position: 'absolute',
        left: 0,
        top: 0,
        width: contentWidth,
        height: contentHeight
    }), [contentWidth, contentHeight]);
    const plugins = usePlugins();
    const sv = sortingViewPlugins(plugins).filter(p => (p.name === 'MVSortingView'))[0];
    if (!sv)
        throw Error('Missing sorting view: MVSortingView');
    const svProps = useMemo(() => (sv.props || {}), [sv.props]);
    const handleGotoRecording = useCallback(() => {
        workspaceRouteDispatch({
            type: 'gotoRecordingPage',
            recordingId: recording.recordingId
        });
    }, [workspaceRouteDispatch, recording.recordingId]);
    if (!sorting) {
        return React.createElement("h3", null, `Sorting not found: ${sortingId}`);
    }
    if (!recording) {
        return React.createElement("h3", null, `Recording not found: ${sorting.recordingId}`);
    }
    if (!recordingInfo) {
        return React.createElement("h3", null, "Loading recording info...");
    }
    if (!sortingInfo) {
        return React.createElement("h3", null, "Loading sorting info...");
    }
    // const selectedUnitIdsLookup: {[key: string]: boolean} = (selection.selectedUnitIds || []).reduce((m, uid) => {m[uid + ''] = true; return m}, {} as {[key: string]: boolean})
    return (React.createElement("div", null,
        React.createElement("div", { style: contentWrapperStyle },
            React.createElement(sv.component, Object.assign({}, svProps, { sorting: sorting, recording: recording, sortingInfo: sortingInfo, recordingInfo: recordingInfo, selection: selection, selectionDispatch: selectionDispatch, curationDispatch: curationDispatch, readOnly: readOnly, calculationPool: calculationPool, width: contentWidth, height: contentHeight }))),
        React.createElement("div", { style: footerStyle },
            `Sorting: `,
            sorting.sortingLabel,
            ` | Recording: `,
            React.createElement(Hyperlink, { onClick: handleGotoRecording }, recording.recordingLabel))));
};
export default SortingView;
//# sourceMappingURL=SortingView.js.map