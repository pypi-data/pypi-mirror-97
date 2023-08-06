import React, { useCallback, useEffect, useMemo, useState } from 'react';
import { FaArrowDown, FaArrowUp } from 'react-icons/fa';
import SortingUnitPlotGrid from '../../common/SortingUnitPlotGrid';
import Splitter from '../../common/Splitter';
import { useRecordingInfo } from '../../common/useRecordingInfo';
import ViewToolbar from '../../common/ViewToolbar';
import AverageWaveformView from './AverageWaveformView';
const TOOLBAR_INITIAL_WIDTH = 36; // hard-coded for now
const AverageWaveformsView = (props) => {
    const { recording, sorting, selection, selectionDispatch, width = 600, height = 650 } = props;
    const recordingInfo = useRecordingInfo(recording.recordingObject);
    const boxHeight = 250;
    const boxWidth = 180;
    const noiseLevel = (recordingInfo || {}).noise_level || 1; // fix this
    const [scalingActions, setScalingActions] = useState(null);
    const unitComponent = useMemo(() => (unitId) => (React.createElement(AverageWaveformView, Object.assign({}, { sorting, recording, unitId, selection, selectionDispatch }, { width: boxWidth, height: boxHeight, noiseLevel: noiseLevel, customActions: scalingActions || [] }))), [sorting, recording, selection, selectionDispatch, noiseLevel, scalingActions]);
    const _handleScaleAmplitudeUp = useCallback(() => {
        selectionDispatch({ type: 'ScaleAmpScaleFactor', direction: 'up' });
    }, [selectionDispatch]);
    const _handleScaleAmplitudeDown = useCallback(() => {
        selectionDispatch({ type: 'ScaleAmpScaleFactor', direction: 'down' });
    }, [selectionDispatch]);
    useEffect(() => {
        const actions = [
            {
                type: 'button',
                callback: _handleScaleAmplitudeUp,
                title: 'Scale amplitude up [up arrow]',
                icon: React.createElement(FaArrowUp, null),
                keyCode: 38
            },
            {
                type: 'button',
                callback: _handleScaleAmplitudeDown,
                title: 'Scale amplitude down [down arrow]',
                icon: React.createElement(FaArrowDown, null),
                keyCode: 40
            }
        ];
        setScalingActions(actions);
    }, [_handleScaleAmplitudeUp, _handleScaleAmplitudeDown]);
    return width ? (React.createElement("div", null,
        React.createElement(Splitter, { width: width, height: height, initialPosition: TOOLBAR_INITIAL_WIDTH, adjustable: false },
            React.createElement(ViewToolbar, { width: TOOLBAR_INITIAL_WIDTH, height: height, customActions: scalingActions }),
            React.createElement(SortingUnitPlotGrid, { sorting: sorting, selection: selection, selectionDispatch: selectionDispatch, unitComponent: unitComponent }))))
        : (React.createElement("div", null, "No width"));
};
export default AverageWaveformsView;
//# sourceMappingURL=AverageWaveformsView.js.map