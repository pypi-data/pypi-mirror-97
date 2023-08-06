import React from 'react';
import { LineSeries, XAxis, XYPlot, YAxis } from 'react-vis';
const SpikeWaveforms_rv = ({ boxSize, plotData, argsObject = { id: 0 }, title }) => {
    if (!plotData.spikes) {
        return React.createElement("div", null);
    }
    const { spikes, sampling_frequency } = plotData;
    const factor = 1000 / sampling_frequency;
    const xAxisLabel = 'dt (msec)';
    return (React.createElement("div", { className: "App", key: "plot-" + argsObject.id },
        React.createElement("div", { style: { textAlign: 'center', fontSize: '12px' } }, title || "Spike waveform(s)"),
        React.createElement(XYPlot, { margin: 30, height: boxSize.height, width: boxSize.width },
            spikes.map((spike, ispike) => {
                const data = spike.waveform.map((v, ii) => ({ x: ii * factor, y: v }));
                return (React.createElement(LineSeries, { key: ispike + '', data: data }));
            }),
            React.createElement(XAxis, null),
            React.createElement(YAxis, null)),
        React.createElement("div", { style: { textAlign: 'center', fontSize: '12px' } }, xAxisLabel)));
};
export default SpikeWaveforms_rv;
//# sourceMappingURL=SpikeWaveforms_rv.js.map