import { Button, Grid } from '@material-ui/core';
import { createCalculationPool, usePlugins } from 'labbox';
import React, { useCallback, useEffect, useMemo, useReducer, useState } from 'react';
import Expandable from '../../common/Expandable';
import Splitter from '../../common/Splitter';
import { useRecordingInfo } from '../../common/useRecordingInfo';
import { recordingSelectionReducer, recordingViewPlugins } from "../../pluginInterface";
import sortByPriority from '../../sortByPriority';
import RecordingInfoView from './RecordingInfoView';
import SortingInstructions from './SortingInstructions';
import SortingsView from './SortingsView';
const calculationPool = createCalculationPool({ maxSimultaneous: 6 });
const WorkspaceRecordingView = ({ recording, sortings, workspaceRoute, workspaceRouteDispatch, onDeleteSortings, width, height }) => {
    const recordingInfo = useRecordingInfo(recording.recordingObject);
    const [showSpikeSortingInstructions, setShowSpikeSortingInstructions] = useState(false);
    const handleSpikeSorting = () => {
        setShowSpikeSortingInstructions(true);
    };
    const initialRecordingSelection = {};
    const [selection, selectionDispatch] = useReducer(recordingSelectionReducer, initialRecordingSelection);
    useEffect(() => {
        if ((!selection.timeRange) && (recordingInfo)) {
            selectionDispatch({ type: 'SetTimeRange', timeRange: { min: 0, max: Math.min(recordingInfo.num_frames, recordingInfo.sampling_frequency / 10) } });
        }
    }, [selection, recordingInfo]);
    const handleBackToRecordings = useCallback(() => {
        workspaceRouteDispatch({
            type: 'gotoRecordingsPage'
        });
    }, [workspaceRouteDispatch]);
    const plugins = usePlugins();
    const rvPlugins = useMemo(() => (recordingViewPlugins(plugins)), [plugins]);
    if (!recordingInfo)
        return React.createElement("div", null, "Loading recording info");
    const content = (React.createElement("div", { style: { margin: 20 } },
        React.createElement(Grid, { container: true, spacing: 3 },
            React.createElement(Grid, { item: true, xs: 12, xl: 6 },
                React.createElement(Button, { onClick: handleBackToRecordings }, "Back to recordings"),
                React.createElement("h2", null, recording.recordingLabel),
                React.createElement("div", null, recording.recordingPath),
                React.createElement(RecordingInfoView, { recordingInfo: recordingInfo, hideElectrodeGeometry: true })),
            React.createElement(Grid, { item: true, xs: 12, xl: 6 },
                React.createElement(SortingsView, { sortings: sortings, workspaceRouteDispatch: workspaceRouteDispatch, workspaceRoute: workspaceRoute, onDeleteSortings: onDeleteSortings }))),
        sortByPriority(rvPlugins).filter(rv => (!rv.disabled)).map(rv => (React.createElement(Expandable, { label: rv.label, defaultExpanded: rv.defaultExpanded ? true : false, key: 'rv-' + rv.name },
            React.createElement(rv.component, { key: 'rvc-' + rv.name, calculationPool: calculationPool, recording: recording, recordingInfo: recordingInfo, selection: selection, selectionDispatch: selectionDispatch, width: width - 40 }))))));
    return (React.createElement(Splitter, Object.assign({}, { width, height }, { initialPosition: 300, positionFromRight: true }),
        React.createElement("div", null,
            !showSpikeSortingInstructions && (React.createElement("div", null,
                React.createElement(Button, { onClick: handleSpikeSorting }, "Spike sorting"))),
            content),
        showSpikeSortingInstructions && (React.createElement(SortingInstructions, { workspaceRoute: workspaceRoute, recordingId: recording.recordingId, recordingLabel: recording.recordingLabel }))));
};
export default WorkspaceRecordingView;
//# sourceMappingURL=WorkspaceRecordingView.js.map