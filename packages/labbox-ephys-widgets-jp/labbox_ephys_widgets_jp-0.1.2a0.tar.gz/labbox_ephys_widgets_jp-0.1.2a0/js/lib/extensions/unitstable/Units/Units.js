var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
import { Button, Paper } from '@material-ui/core';
import { HitherContext, usePlugins } from 'labbox';
import React, { useCallback, useContext, useEffect, useMemo, useReducer, useState } from 'react';
import { useSortingInfo } from '../../common/useSortingInfo';
import { sortingUnitMetricPlugins } from "../../pluginInterface";
import sortByPriority from '../../sortByPriority';
import UnitsTable from './UnitsTable';
const initialMetricDataState = {};
const updateMetricData = (state, action) => {
    if (action === 'clear')
        return {};
    const { metricName, status, data, error } = action;
    if (state[metricName] && state[metricName].status === 'completed') {
        console.warn(`Updating status of completed metric ${metricName}??`);
        return state;
    }
    return Object.assign(Object.assign({}, state), { [metricName]: {
            'status': status,
            'data': status === 'completed' ? data || null : null,
            'error': status === 'error' ? error || null : null
        } });
};
const Units = (props) => {
    const hither = useContext(HitherContext);
    const { sorting, recording, selection, selectionDispatch, width, height } = props;
    const [expandedTable, setExpandedTable] = useState(false);
    const [metrics, updateMetrics] = useReducer(updateMetricData, initialMetricDataState);
    const [previousRecording, setPreviousRecording] = useState(null);
    useEffect(() => {
        if (previousRecording !== recording) {
            updateMetrics('clear');
            setPreviousRecording(recording);
        }
    }, [recording, previousRecording, setPreviousRecording, updateMetrics]);
    const fetchMetric = useCallback((metric) => __awaiter(void 0, void 0, void 0, function* () {
        const name = metric.name;
        if (name in metrics) {
            return metrics[name];
        }
        // TODO: FIXME! THIS STATE IS NOT PRESERVED BETWEEN UNFOLDINGS!!!
        // TODO: May need to bump this up to the parent!!!
        // new request. Add state to cache, dispatch job, then update state as results come back.
        updateMetrics({ metricName: metric.name, status: 'executing' });
        try {
            const data = yield hither.createHitherJob(metric.hitherFnName, {
                sorting_object: sorting.sortingObject,
                recording_object: recording.recordingObject,
                configuration: metric.metricFnParams
            }, metric.hitherOpts).wait();
            updateMetrics({ metricName: metric.name, status: 'completed', data });
        }
        catch (err) {
            console.error(err);
            updateMetrics({ metricName: metric.name, status: 'error', error: err.message });
        }
    }), [metrics, sorting.sortingObject, recording.recordingObject, hither]);
    const plugins = usePlugins();
    useEffect(() => {
        sortByPriority(sortingUnitMetricPlugins(plugins)).filter(p => (!p.disabled)).forEach((mp) => __awaiter(void 0, void 0, void 0, function* () { return yield fetchMetric(mp); }));
    }, [plugins, metrics, fetchMetric]);
    const metricsPlugins = useMemo(() => (sortingUnitMetricPlugins(plugins)), [plugins]);
    const sortingInfo = useSortingInfo(sorting.sortingObject, sorting.recordingObject);
    if (!sortingInfo)
        return React.createElement("div", null, "No sorting info");
    let units = selection.visibleUnitIds || sortingInfo.unit_ids;
    let showExpandButton = false;
    if ((!expandedTable) && (units.length > 30)) {
        units = units.slice(0, 30);
        showExpandButton = true;
    }
    return (React.createElement("div", { style: { width: width || 300 } },
        React.createElement(Paper, { style: { maxHeight: props.maxHeight, overflow: 'auto' } },
            React.createElement(UnitsTable, { sortingUnitMetrics: metricsPlugins, units: units, metrics: metrics, selection: selection, selectionDispatch: selectionDispatch, sorting: sorting, height: height }),
            showExpandButton && (React.createElement(Button, { onClick: () => { setExpandedTable(true); } }, "Show all units")))));
};
export default Units;
//# sourceMappingURL=Units.js.map