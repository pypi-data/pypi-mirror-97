var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
import { createCalculationPool, HitherContext } from 'labbox';
import { useContext, useMemo } from "react";
import useFetchCache from "../../common/useFetchCache";
// it may be important to limit this when using a filter
const timeseriesCalculationPool = createCalculationPool({ maxSimultaneous: 4, method: 'stack' });
const getTimeseriesDataSegment = (args) => __awaiter(void 0, void 0, void 0, function* () {
    const { hither, recordingObject, ds_factor, segment_num, segment_size } = args;
    const result = yield hither.createHitherJob('createjob_get_timeseries_segment', {
        recording_object: recordingObject,
        ds_factor,
        segment_num,
        segment_size
    }, {
        useClientCache: true,
        calculationPool: timeseriesCalculationPool
    }).wait();
    return result.traces;
});
const useTimeseriesData = (recordingObject, recordingInfo) => {
    const hither = useContext(HitherContext);
    const fetch = useMemo(() => ((query) => __awaiter(void 0, void 0, void 0, function* () {
        switch (query.type) {
            case 'dataSegment': {
                return yield getTimeseriesDataSegment({ hither, recordingObject, ds_factor: query.ds_factor, segment_num: query.segment_num, segment_size: query.segment_size });
            }
        }
    })), [hither, recordingObject]);
    const data = useFetchCache(fetch);
    const segment_size_times_num_channels = 100000;
    const num_channels = recordingInfo.channel_ids.length;
    const segment_size = Math.ceil(segment_size_times_num_channels / num_channels);
    const getChannelData = useMemo(() => ((ch, t1, t2, ds_factor) => {
        // Here we are retrieving the channel data, between for timepoints [t1, t2), with downsampling factor ds_factor
        // first we accumulate the information about which segments we need to retrieve
        const i1 = Math.floor(Math.max(0, t1) / segment_size); // index of start segment
        const i2 = Math.ceil((Math.min(t2, recordingInfo.num_frames) - 1) / segment_size); // index of end segment (inclusive)
        const segments = [];
        for (let i = i1; i <= i2; i++) {
            if ((i === i1) && (i === i2)) {
                // There is only one segment
                segments.push({
                    segment_num: i,
                    t1: i * segment_size,
                    t2: (i + 1) * segment_size,
                    src1: t1 - (i * segment_size),
                    src2: t2 - (i * segment_size),
                    dst1: 0,
                    dst2: t2 - t1 // [t2 - t1] - 0 ?= [t2 - (i * segment_size)] - [t1 - (i * segment_size)] YES
                });
            }
            else if (i === i1) {
                // There's more than one segment, and this is the first one
                segments.push({
                    segment_num: i,
                    t1: i * segment_size,
                    t2: (i + 1) * segment_size,
                    src1: t1 - (i * segment_size),
                    src2: segment_size,
                    dst1: 0,
                    dst2: segment_size + (i * segment_size) - t1 // [segment_size + (i * segment_size) - t1] - 0 ?= [segment_size] - [t1 - (i * segment_size)] YES
                });
            }
            else if (i === i2) {
                // There's more than one segment, and this is the last one
                segments.push({
                    segment_num: i,
                    t1: i * segment_size,
                    t2: (i + 1) * segment_size,
                    src1: 0,
                    src2: t2 - (i * segment_size),
                    dst1: i * segment_size - t1,
                    dst2: t2 - t1 // [t2 - t1] - [i * segment_size - t1] ?= [t2 - (i * segment_size)] - 0 YES
                });
            }
            else {
                // There's more than one segment, and we are in the middle
                segments.push({
                    segment_num: i,
                    t1: i * segment_size,
                    t2: (i + 1) * segment_size,
                    src1: 0,
                    src2: segment_size,
                    dst1: i * segment_size - t1,
                    dst2: (i + 1) * segment_size - t1 // [(i + 1) * segment_size - t1] - [i * segment_size - t1] ?= [segment_size] - 0 YES
                });
            }
        }
        // This is the output array, which may get some NaN's if the segments are not yet available
        const ret = [];
        if (ds_factor === 1) {
            // In this case we are not downsampling
            // start out filling with NaN's
            for (let t = t1; t < t2; t++) {
                ret.push(NaN);
            }
            // Loop through the segments and copy the data into the output array
            for (let segment of segments) {
                const x = data.get({ type: 'dataSegment', ds_factor, segment_num: segment.segment_num, segment_size });
                // x will be undefined if that segment is not yet on the client - in that case the fetch request will be triggered, if not already in process
                if (x) {
                    // the data is on the client
                    for (let i = 0; i < segment.src2 - segment.src1; i++) {
                        // read from the input and write to the output according to the prepared offsets
                        // note that we don't actually need src2 and dst2, but it doesn't hurt to have them for clarity
                        ret[segment.dst1 + i] = x[ch][segment.src1 + i];
                    }
                }
            }
        }
        else {
            // In this case we are downsampling, so we double the size, storing the mins and the maxs over the ds step size
            for (let t = t1; t < t2; t++) {
                ret.push(NaN);
                ret.push(NaN);
            }
            // Loop through the segments and copy the data into the output array
            for (let segment of segments) {
                const x = data.get({ type: 'dataSegment', ds_factor, segment_num: segment.segment_num, segment_size });
                // x will be undefined if that segment is not yet on the client - in that case the fetch request will be triggered, if not already in process
                if (x) {
                    // the data is on the client
                    for (let i = 0; i < segment.src2 - segment.src1; i++) {
                        // read from the input and write to the output according to the prepared offsets
                        // note that we don't actually need src2 and dst2, but it doesn't hurt to have them for clarity
                        ret[(segment.dst1 + i) * 2] = x[ch][(segment.src1 + i) * 2];
                        ret[(segment.dst1 + i) * 2 + 1] = x[ch][(segment.src1 + i) * 2 + 1];
                    }
                }
            }
        }
        return ret;
    }), [data, recordingInfo.num_frames, segment_size]);
    return useMemo(() => ({
        getChannelData,
        requestChannelData: getChannelData,
        numChannels: () => (recordingInfo.channel_ids.length),
        numTimepoints: () => (recordingInfo.num_frames),
        getSampleRate: () => (recordingInfo.sampling_frequency)
    }), [getChannelData, recordingInfo]);
};
export default useTimeseriesData;
//# sourceMappingURL=useTimeseriesModel.js.map