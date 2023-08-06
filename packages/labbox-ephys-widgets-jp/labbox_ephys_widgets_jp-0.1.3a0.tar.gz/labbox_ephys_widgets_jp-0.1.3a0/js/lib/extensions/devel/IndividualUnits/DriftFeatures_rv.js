import React from 'react';
import { MarkSeries, XAxis, XYPlot, YAxis } from 'react-vis';
const DriftFeatures_rv = ({ boxSize, plotData, argsObject = { id: 0, onPointClicked: null }, title }) => {
    // plotData: {times, features, labels}
    // console.log(plotData);
    if (!plotData.features) {
        // assume no events
        return React.createElement("div", null);
    }
    const xAxisLabel = 'Time (min)';
    const yAxisLabel = 'PCA 1';
    const { times, features, labels } = plotData;
    const data = features[0].map((v, ii) => ({ index: ii, x: times[ii] / 60, y: features[0][ii], color: labels[ii] }));
    const _handlePointClick = (event) => {
        argsObject.onPointClicked && argsObject.onPointClicked({ index: event.index });
    };
    return (React.createElement("div", { className: "App", key: "plot-" + argsObject.id },
        React.createElement("div", { style: { textAlign: 'center', fontSize: '12px' } }, title || "Waveform features over time"),
        React.createElement(XYPlot, { margin: 30, height: boxSize.height, width: boxSize.width },
            React.createElement(MarkSeries, { data: data, stroke: "black", 
                // size={4}
                onValueClick: event => _handlePointClick(event) }),
            React.createElement(XAxis, { title: xAxisLabel }),
            React.createElement(YAxis, { title: yAxisLabel }))));
};
export default DriftFeatures_rv;
//# sourceMappingURL=DriftFeatures_rv.js.map