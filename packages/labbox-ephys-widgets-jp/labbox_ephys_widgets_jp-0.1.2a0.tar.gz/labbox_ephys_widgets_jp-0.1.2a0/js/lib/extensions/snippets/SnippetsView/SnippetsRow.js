var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
import { GridList, GridListTile } from '@material-ui/core';
import { createCalculationPool, HitherContext } from 'labbox';
import React, { useContext, useMemo } from 'react';
import { getElectrodesAspectRatio } from '../../averagewaveforms/AverageWaveformsView/setupElectrodes';
import useFetchCache from '../../common/useFetchCache';
import { applyMergesToUnit } from "../../pluginInterface";
import SnippetBox from './SnippetBox';
const calculationPool = createCalculationPool({ maxSimultaneous: 6 });
const getSnippetsInfo = (args) => __awaiter(void 0, void 0, void 0, function* () {
    const { recording, sorting, unitId, hither } = args;
    const result = yield hither.createHitherJob('createjob_get_sorting_unit_info', {
        recording_object: recording.recordingObject,
        sorting_object: sorting.sortingObject,
        unit_id: unitId
    }, {
        useClientCache: true,
        calculationPool
    }).wait();
    return {
        channel_ids: result.channel_ids,
        channel_locations: result.channel_locations,
        sampling_frequency: result.sampling_frequency
    };
});
const getSnippets = (args) => __awaiter(void 0, void 0, void 0, function* () {
    const { recording, sorting, unitId, timeRange, hither } = args;
    const result = yield hither.createHitherJob('createjob_get_sorting_unit_snippets', {
        recording_object: recording.recordingObject,
        sorting_object: sorting.sortingObject,
        unit_id: unitId,
        time_range: timeRange,
        max_num_snippets: 1000
    }, {
        useClientCache: true,
        calculationPool
    }).wait();
    return result.snippets;
});
const segmentSize = 30000 * 10;
const createTimeSegments = (timeRange, opts) => {
    const ret = [];
    if (!timeRange)
        return ret;
    const i1 = Math.floor(timeRange.min / segmentSize);
    const i2 = Math.ceil(timeRange.max / segmentSize);
    for (let i = i1; i <= Math.min(i2, i1 + opts.maxNumSegments - 1); i++) {
        ret.push({ min: i * segmentSize, max: (i + 1) * segmentSize });
    }
    return ret;
};
const useSnippets = (args) => {
    const hither = useContext(HitherContext);
    const { recording, sorting, selection, visibleElectrodeIds, unitId, timeRange } = args;
    const fetchFunction = useMemo(() => ((query) => __awaiter(void 0, void 0, void 0, function* () {
        switch (query.type) {
            case 'info':
                const uid1 = applyMergesToUnit(query.unitId, sorting.curation, selection.applyMerges);
                return yield getSnippetsInfo({ recording: query.recording, sorting: query.sorting, unitId: uid1, hither });
            case 'snippets':
                const uid2 = applyMergesToUnit(query.unitId, sorting.curation, selection.applyMerges);
                return yield getSnippets({ recording: query.recording, sorting: query.sorting, unitId: uid2, timeRange: query.timeRange, hither });
        }
    })), [hither, sorting.curation, selection.applyMerges]);
    const data = useFetchCache(fetchFunction);
    return useMemo(() => {
        const infoQuery = { type: 'info', recording, sorting, unitId };
        // const snippetsQuery: SnippetsQuery = {type: 'snippets', recording, sorting, unitId}
        const info = data.get(infoQuery);
        const timeSegments = createTimeSegments(timeRange, { maxNumSegments: 6 });
        const snippetsList = timeSegments.map(timeSegment => {
            const snippetsQuery = {
                type: 'snippets',
                recording,
                sorting,
                unitId,
                timeRange: timeSegment
            };
            return data.get(snippetsQuery);
        })
            .reduce((acc, val) => (val ? (acc.concat(val)) : acc), []); // accumulate the snippets from the time segments
        const snippets = snippetsList.map(s => (filterSnippetVisibleElectrodes(s, info === null || info === void 0 ? void 0 : info.channel_ids, visibleElectrodeIds) // only show the visible electrodes
        ));
        const snippetsInRange = snippets ? (snippets.filter((s) => ((timeRange) && (timeRange.min <= s.timepoint) && (s.timepoint < timeRange.max)))) : undefined;
        return {
            info: info ? Object.assign(Object.assign({}, info), { channel_ids: info.channel_ids.filter((eid, ii) => ((!visibleElectrodeIds) || (visibleElectrodeIds.includes(info.channel_ids[ii])))), channel_locations: info.channel_locations.filter((loc, ii) => ((!visibleElectrodeIds) || (visibleElectrodeIds.includes(info.channel_ids[ii])))) }) : undefined,
            snippets: snippetsInRange
        };
    }, [data, recording, sorting, timeRange, unitId, visibleElectrodeIds]);
};
const filterSnippetVisibleElectrodes = (s, electrodeIds, visibleElectrodeIds) => {
    var _a;
    if (!electrodeIds)
        return s;
    if (!visibleElectrodeIds)
        return s;
    return Object.assign(Object.assign({}, s), { waveform: (_a = s.waveform) === null || _a === void 0 ? void 0 : _a.filter((x, i) => (visibleElectrodeIds.includes(electrodeIds[i]))) });
};
const SnippetsRow = ({ recording, sorting, selection, selectionDispatch, unitId, height, noiseLevel }) => {
    const { snippets, info } = useSnippets({ recording, sorting, selection, visibleElectrodeIds: selection.visibleElectrodeIds, unitId, timeRange: selection.timeRange || null });
    const electrodeLocations = info === null || info === void 0 ? void 0 : info.channel_locations;
    const boxWidth = useMemo(() => {
        if (selection.waveformsMode === 'geom') {
            const boxAspect = (electrodeLocations ? getElectrodesAspectRatio(electrodeLocations) : 1) || 1;
            return (boxAspect > 1 ? height / boxAspect : height * boxAspect);
        }
        else {
            return 100;
        }
    }, [electrodeLocations, height, selection.waveformsMode]);
    const tileStyle = useMemo(() => ({ width: boxWidth + 5, height: height + 15 }), [boxWidth, height]);
    return (React.createElement(GridList, { style: { flexWrap: 'nowrap', height: height + 15 } }, info && electrodeLocations && snippets ? (snippets.length > 0 ? (snippets.map((snippet) => (React.createElement(GridListTile, { key: snippet.timepoint, style: tileStyle },
        React.createElement(SnippetBox, { snippet: snippet, noiseLevel: noiseLevel, samplingFrequency: info.sampling_frequency, electrodeIds: info.channel_ids, electrodeLocations: electrodeLocations, selection: selection, selectionDispatch: selectionDispatch, width: boxWidth, height: height }))))) : (React.createElement(GridListTile, { style: Object.assign(Object.assign({}, tileStyle), { width: 500, color: 'gray' }) },
        React.createElement("div", null, "No snippets found in selected time range")))) : (React.createElement(GridListTile, { style: Object.assign(Object.assign({}, tileStyle), { width: 180 }) },
        React.createElement("div", { style: { whiteSpace: 'nowrap' } }, "Retrieving snippets...")))));
};
export default SnippetsRow;
//# sourceMappingURL=SnippetsRow.js.map