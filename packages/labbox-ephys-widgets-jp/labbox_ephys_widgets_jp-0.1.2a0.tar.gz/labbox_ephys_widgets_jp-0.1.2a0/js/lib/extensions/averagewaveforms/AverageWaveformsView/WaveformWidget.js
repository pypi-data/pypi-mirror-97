import React from 'react';
import CanvasWidget from '../../common/CanvasWidget';
import { useLayer, useLayers } from '../../common/CanvasWidget/CanvasWidgetLayer';
import { createElectrodesLayer } from './electrodesLayer';
import { createWaveformLayer } from './waveformLayer';
const electrodeColors = {
    border: 'rgb(120, 100, 120)',
    base: 'rgb(255, 255, 255)',
    selected: 'rgb(196, 196, 128)',
    hover: 'rgb(128, 128, 255)',
    selectedHover: 'rgb(200, 200, 196)',
    dragged: 'rgb(0, 0, 196)',
    draggedSelected: 'rgb(180, 180, 150)',
    dragRect: 'rgba(196, 196, 196, 0.5)',
    textLight: 'rgb(32, 32, 32)',
    textDark: 'rgb(228, 228, 228)'
};
const waveformColors = {
    base: 'black'
};
const defaultElectrodeOpts = {
    colors: electrodeColors,
    showLabels: false
};
const defaultWaveformOpts = {
    colors: waveformColors,
    waveformWidth: 2
};
const WaveformWidget = (props) => {
    const layerProps = Object.assign(Object.assign({}, props), { electrodeOpts: Object.assign(Object.assign({}, defaultElectrodeOpts), props.electrodeOpts), waveformOpts: defaultWaveformOpts });
    const electrodeLayerProps = Object.assign(Object.assign({}, props), { electrodeOpts: Object.assign(Object.assign({}, defaultElectrodeOpts), props.electrodeOpts) });
    const electrodesLayer = useLayer(createElectrodesLayer, electrodeLayerProps);
    const waveformLayer = useLayer(createWaveformLayer, layerProps);
    const layers = useLayers([electrodesLayer, waveformLayer]);
    return (React.createElement(CanvasWidget, Object.assign({ layers: layers }, { width: props.width, height: props.height })));
};
export default WaveformWidget;
//# sourceMappingURL=WaveformWidget.js.map