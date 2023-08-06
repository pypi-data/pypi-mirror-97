import { Grid } from '@material-ui/core';
import React, { Fragment, useCallback, useState } from 'react';
import VisibilitySensor from 'react-visibility-sensor';
import { useRecordingInfo } from '../../common/useRecordingInfo';
import SnippetsRow from './SnippetsRow';
const WhenVisible = ({ width, height, children }) => {
    const [hasBeenVisible, setHasBeenVisible] = useState(false);
    const handleVisibilityChange = useCallback((isVisible) => {
        if ((isVisible) && (!hasBeenVisible))
            setHasBeenVisible(true);
    }, [hasBeenVisible, setHasBeenVisible]);
    return hasBeenVisible ? React.createElement(Fragment, null, children) : (React.createElement(VisibilitySensor, { onChange: handleVisibilityChange, partialVisibility: true },
        React.createElement("div", { className: "WhenVisible", style: { position: 'absolute', width, height } }, "Waiting for visible")));
};
const SnippetsWidget = ({ recording, sorting, selection, selectionDispatch, unitIds, width, height }) => {
    const recordingInfo = useRecordingInfo(recording.recordingObject);
    const noiseLevel = (recordingInfo || {}).noise_level || 1; // fix this
    const rowHeight = 250;
    return (React.createElement("div", { style: { position: 'absolute', width, height, overflow: 'auto' } },
        React.createElement(Grid, { container: true, direction: "column" }, (unitIds || []).map(unitId => (React.createElement(Grid, { item: true, key: unitId, style: { border: 'solid 3px lightgray', marginBottom: 2 } },
            React.createElement("h3", { style: { paddingTop: 0, paddingBottom: 0, marginTop: 10, marginBottom: 10 } },
                "Snippets for unit ",
                unitId),
            React.createElement(WhenVisible, { width: width, height: rowHeight },
                React.createElement(SnippetsRow, Object.assign({}, { recording, sorting, selection, selectionDispatch, unitId, height: rowHeight, noiseLevel })))))))));
};
export default SnippetsWidget;
//# sourceMappingURL=SnippetsWidget.js.map