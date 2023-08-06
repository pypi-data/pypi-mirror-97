var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
import { Box, CircularProgress } from '@material-ui/core';
import { HitherContext } from 'labbox';
import React, { useContext, useEffect, useState } from 'react';
import VisibilitySensor from 'react-visibility-sensor';
const ClientSidePlot = ({ dataFunctionName, dataFunctionArgs, calculationPool, boxSize = { width: 200, height: 200 }, PlotComponent, plotComponentArgs, plotComponentProps, title }) => {
    const hither = useContext(HitherContext);
    const [calculationStatus, setCalculationStatus] = useState('waitingForVisible');
    const [calculationError, setCalculationError] = useState(null);
    const [plotData, setPlotData] = useState(null);
    const [visible, setVisible] = useState(false);
    useEffect(() => {
        ;
        (() => __awaiter(void 0, void 0, void 0, function* () {
            if ((calculationStatus === 'waitingForVisible') && (visible)) {
                setCalculationStatus('waiting');
                const slot = calculationPool ? yield calculationPool.requestSlot() : null;
                setCalculationStatus('calculating');
                let plot_data;
                try {
                    plot_data = yield hither.createHitherJob(dataFunctionName, dataFunctionArgs, {
                        useClientCache: true
                    }).wait();
                }
                catch (err) {
                    console.error(err);
                    setCalculationError(err.message);
                    setCalculationStatus('error');
                    return;
                }
                finally {
                    slot && slot.complete();
                }
                setPlotData(plot_data);
                setCalculationStatus('finished');
            }
        }))();
    }, [dataFunctionName, calculationStatus, calculationPool, dataFunctionArgs, hither, visible]);
    if (calculationStatus === 'waitingForVisible') {
        return (React.createElement(VisibilitySensor, { partialVisibility: true }, ({ isVisible }) => {
            if (isVisible) {
                // the setTimeout may be needed here to prevent a warning message
                setTimeout(() => {
                    setVisible(true);
                }, 0);
            }
            else {
                // the setTimeout may be needed here to prevent a warning message
                setTimeout(() => {
                    setVisible(false);
                }, 0);
            }
            return (React.createElement(Box, { display: "flex", width: boxSize.width, height: boxSize.height },
                React.createElement(Box, { m: "auto" },
                    React.createElement("div", null, "waiting-for-visible"))));
        }));
    }
    if (calculationStatus === 'pending' || calculationStatus === 'waiting') {
        return (React.createElement(Box, { display: "flex", width: boxSize.width, height: boxSize.height }));
    }
    else if (calculationStatus === 'calculating') {
        return (React.createElement(Box, { display: "flex", width: boxSize.width, height: boxSize.height },
            React.createElement(Box, { m: "auto" },
                React.createElement(CircularProgress, null))));
    }
    else if (calculationStatus === 'error') {
        return (React.createElement(Box, { display: "flex", width: boxSize.width, height: boxSize.height },
            React.createElement(Box, { m: "auto" },
                React.createElement("div", null,
                    "Error in calculation: ",
                    React.createElement("pre", null, calculationError)))));
    }
    else if ((calculationStatus === 'finished') && (plotData)) {
        // TODO: Follow-up on distinction b/w this and <PlotComponent arg1={} arg2={} ... />
        return React.createElement(PlotComponent, Object.assign({}, Object.assign(Object.assign({ boxSize, plotData, argsObject: plotComponentArgs }, (plotComponentProps || {})), { title })));
    }
    else {
        return (React.createElement("div", null,
            "Unexpected calculation status: ",
            calculationStatus));
    }
};
export default ClientSidePlot;
//# sourceMappingURL=ClientSidePlot.js.map