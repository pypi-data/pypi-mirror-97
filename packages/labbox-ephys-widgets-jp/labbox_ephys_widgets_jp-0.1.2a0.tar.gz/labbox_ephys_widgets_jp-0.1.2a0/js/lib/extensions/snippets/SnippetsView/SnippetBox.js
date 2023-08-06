import React, { useCallback, useMemo, useState } from 'react';
import VisibilitySensor from 'react-visibility-sensor';
import WaveformWidget from '../../averagewaveforms/AverageWaveformsView/WaveformWidget';
const SnippetBox = ({ snippet, noiseLevel, samplingFrequency, electrodeIds, electrodeLocations, selection, selectionDispatch, width, height }) => {
    const [hasBeenVisible, setHasBeenVisible] = useState(false);
    const handleVisibilityChange = useCallback((isVisible) => {
        if ((isVisible) && (!hasBeenVisible))
            setHasBeenVisible(true);
    }, [hasBeenVisible, setHasBeenVisible]);
    const snippetTimepoint = (snippet === null || snippet === void 0 ? void 0 : snippet.timepoint) || 0;
    const currentTimepoint = selection.currentTimepoint || 0;
    const selected = useMemo(() => (Math.abs(snippetTimepoint - currentTimepoint) < 20), [snippetTimepoint, currentTimepoint]);
    const handleClick = useCallback(() => {
        snippet && selectionDispatch({ type: 'SetCurrentTimepoint', currentTimepoint: snippet.timepoint });
    }, [snippet, selectionDispatch]);
    return (React.createElement(VisibilitySensor, { onChange: handleVisibilityChange, partialVisibility: true }, hasBeenVisible && snippet ? (React.createElement("div", { className: selected ? "plotSelectedStyle" : "", onClick: handleClick },
        React.createElement(WaveformWidget, Object.assign({ waveform: snippet.waveform, layoutMode: selection.waveformsMode || 'geom' }, { selection, selectionDispatch, noiseLevel, samplingFrequency, electrodeIds, electrodeLocations, width, height }, { electrodeOpts: { disableSelection: true } })))) : (React.createElement("div", { style: { position: 'absolute', width, height } }))));
};
export default SnippetBox;
//# sourceMappingURL=SnippetBox.js.map