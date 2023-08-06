import React, { useCallback } from 'react';
import Splitter from '../../common/Splitter';
import useTimeseriesData from '../../timeseries/TimeseriesViewNew/useTimeseriesModel';
import FireTrackWidget from './FireTrackWidget';
const FireTrackView = ({ recording, recordingInfo, sorting, selection, selectionDispatch, width, height }) => {
    var _a;
    const handleStopAnimation = useCallback((args) => {
        selectionDispatch({ type: 'SetCurrentTimepointVelocity', velocity: 0 });
    }, [selectionDispatch]);
    const handleStartAnimation = useCallback((args) => {
        selectionDispatch({ type: 'SetCurrentTimepointVelocity', velocity: 50 });
    }, [selectionDispatch]);
    const timeseriesData = useTimeseriesData(recording.recordingObject, recordingInfo);
    return (React.createElement(Splitter, { width: width || 400, height: height || 400, initialPosition: 150 },
        React.createElement("div", null, ((_a = selection.animation) === null || _a === void 0 ? void 0 : _a.currentTimepointVelocity) ? (React.createElement("button", { onClick: handleStopAnimation }, "Stop animation")) : (React.createElement("button", { onClick: handleStartAnimation }, "Start animation"))),
        React.createElement(FireTrackWidget, Object.assign({}, { recording, timeseriesData, selection }, { width: 0, height: 0 }))));
};
export default FireTrackView;
//# sourceMappingURL=FireTrackView.js.map