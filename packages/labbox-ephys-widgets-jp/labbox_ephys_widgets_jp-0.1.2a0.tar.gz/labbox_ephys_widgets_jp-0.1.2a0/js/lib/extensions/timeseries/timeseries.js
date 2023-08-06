// LABBOX-EXTENSION: timeseries
// LABBOX-EXTENSION-TAGS: jupyter
import TimelineIcon from '@material-ui/icons/Timeline';
import React from 'react';
import TimeseriesViewNew from './TimeseriesViewNew/TimeseriesViewNew';
const TimeseriesSortingView = ({ recording, recordingInfo, width, height, selection, selectionDispatch }) => {
    return (React.createElement(TimeseriesViewNew, { recordingObject: recording.recordingObject, recordingInfo: recordingInfo, width: width || 600, height: height || 600, opts: { channelSelectPanel: true }, recordingSelection: selection, recordingSelectionDispatch: selectionDispatch }));
};
const TimeseriesRecordingView = ({ recording, recordingInfo, width, height, selection, selectionDispatch }) => {
    return (React.createElement(TimeseriesViewNew, { recordingObject: recording.recordingObject, recordingInfo: recordingInfo, width: width || 600, height: height || 600, opts: { channelSelectPanel: true }, recordingSelection: selection, recordingSelectionDispatch: selectionDispatch }));
};
export function activate(context) {
    context.registerPlugin({
        type: 'RecordingView',
        name: 'TimeseriesView',
        label: 'Timeseries',
        priority: 50,
        fullWidth: true,
        component: TimeseriesRecordingView
    });
    context.registerPlugin({
        type: 'SortingView',
        name: 'TimeseriesView',
        label: 'Timeseries',
        priority: 50,
        component: TimeseriesSortingView,
        icon: React.createElement(TimelineIcon, null)
    });
}
//# sourceMappingURL=timeseries.js.map