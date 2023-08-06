import { CircularProgress } from '@material-ui/core';
import React, { useCallback, useMemo } from 'react';
import NiceTable from '../../common/NiceTable';
import { useRecordingInfos } from '../../common/useRecordingInfo';
import './WorkspaceView.css';
const sortingElement = (sorting, sortingInfo) => {
    return React.createElement("span", { key: sorting.sortingId },
        sorting.sortingId,
        " (",
        sortingInfo ? sortingInfo.unit_ids.length : '',
        ")");
};
const sortingsElement = (sortings) => {
    return (React.createElement("span", null, sortings.map(s => (sortingElement(s)))));
};
const RecordingsTable = ({ recordings, sortings, onDeleteRecordings, readOnly, workspaceRouteDispatch }) => {
    const sortingsByRecordingId = useMemo(() => {
        const ret = {};
        recordings.forEach(r => {
            ret[r.recordingId] = sortings.filter(s => (s.recordingId === r.recordingId));
        });
        return ret;
    }, [recordings, sortings]);
    function sortByKey(array, key) {
        return array.sort(function (a, b) {
            var x = a[key];
            var y = b[key];
            return ((x < y) ? -1 : ((x > y) ? 1 : 0));
        });
    }
    recordings = sortByKey(recordings, 'recordingLabel');
    const handleViewRecording = useCallback((recording) => {
        workspaceRouteDispatch({
            type: 'gotoRecordingPage',
            recordingId: recording.recordingId
        });
    }, [workspaceRouteDispatch]);
    const recordingInfos = useRecordingInfos(recordings);
    const rows = useMemo(() => (recordings.map(rec => {
        const recordingInfo = recordingInfos[rec.recordingId];
        return {
            key: rec.recordingId,
            columnValues: {
                recording: rec,
                recordingLabel: {
                    text: rec.recordingLabel,
                    element: React.createElement(ViewRecordingLink, { onClick: handleViewRecording, recording: rec }),
                },
                numChannels: recordingInfo ? recordingInfo.channel_ids.length : { element: React.createElement(CircularProgress, null) },
                samplingFrequency: recordingInfo ? recordingInfo.sampling_frequency : '',
                durationMinutes: recordingInfo ? recordingInfo.num_frames / recordingInfo.sampling_frequency / 60 : '',
                sortings: { element: sortingsElement(sortingsByRecordingId[rec.recordingId]) }
            }
        };
    })), [recordings, sortingsByRecordingId, handleViewRecording, recordingInfos]);
    const handleDeleteRow = useCallback((key) => {
        onDeleteRecordings && onDeleteRecordings([key]);
    }, [onDeleteRecordings]);
    const columns = [
        {
            key: 'recordingLabel',
            label: 'Recording'
        },
        {
            key: 'numChannels',
            label: 'Num. channels'
        },
        {
            key: 'samplingFrequency',
            label: 'Samp. freq. (Hz)'
        },
        {
            key: 'durationMinutes',
            label: 'Duration (min)'
        },
        {
            key: 'sortings',
            label: 'Sortings'
        }
    ];
    return (React.createElement("div", null,
        React.createElement(NiceTable, { rows: rows, columns: columns, deleteRowLabel: "Remove this recording", onDeleteRow: readOnly ? undefined : handleDeleteRow })));
};
const ViewRecordingLink = ({ recording, onClick }) => {
    const handleClick = useCallback(() => {
        onClick(recording);
    }, [recording, onClick]);
    return (React.createElement(Anchor, { title: "View recording", onClick: handleClick }, recording.recordingLabel));
};
const Anchor = ({ title, children, onClick }) => {
    return (React.createElement("button", { type: "button", className: "link-button", onClick: onClick }, children));
};
export default RecordingsTable;
//# sourceMappingURL=RecordingsTable.js.map