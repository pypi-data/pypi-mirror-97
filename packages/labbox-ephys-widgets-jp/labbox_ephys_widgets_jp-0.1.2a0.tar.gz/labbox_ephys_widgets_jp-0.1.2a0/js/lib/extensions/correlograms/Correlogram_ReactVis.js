import React from 'react';
import { VerticalBarSeries, XAxis, XYPlot, YAxis } from 'react-vis';
const Correlogram_rv = ({ boxSize, plotData, argsObject = { id: 0 }, title }) => {
    // plotData will be an array of [x-vals], [y-vals], and x-stepsize.
    // need to convert to an array of objects with x-y pairs.
    // We'll be doing this a LOT, it belongs elsewhere
    if (!plotData) {
        return React.createElement("div", null, "No data");
    }
    const data = plotData[0].map((item, index) => {
        return { x: item, y: plotData[1][index] };
    });
    const xAxisLabel = 'dt (msec)';
    return (React.createElement("div", { className: "App", key: "plot-" + argsObject.id },
        React.createElement("div", { style: { textAlign: 'center', fontSize: '12px' } }, title),
        React.createElement(XYPlot, { margin: 30, height: boxSize.height, width: boxSize.width },
            React.createElement(VerticalBarSeries, { data: data, barWidth: 1 }),
            React.createElement(XAxis, null),
            React.createElement(YAxis, null)),
        React.createElement("div", { style: { textAlign: 'center', fontSize: '12px' } }, xAxisLabel)));
};
export default Correlogram_rv;
//# sourceMappingURL=Correlogram_ReactVis.js.map