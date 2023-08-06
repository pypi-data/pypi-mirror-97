var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
import { createCalculationPool, HitherContext } from "labbox/lib/hither";
import { useContext, useMemo } from "react";
import useFetchCache from "../../common/useFetchCache";
import { getArrayMax, getArrayMin } from '../../common/Utility';
const calculationPool = createCalculationPool({ maxSimultaneous: 6 });
const fetchSpikeAmplitudes = ({ hither, recordingObject, sortingObject, unitId }) => __awaiter(void 0, void 0, void 0, function* () {
    const result = yield hither.createHitherJob('createjob_fetch_spike_amplitudes', {
        recording_object: recordingObject,
        sorting_object: sortingObject,
        unit_id: unitId
    }, {
        useClientCache: true,
        calculationPool
    }).wait();
    return Object.assign(Object.assign({}, result), { minAmp: getArrayMin(result.amplitudes), maxAmp: getArrayMax(result.amplitudes) });
});
const useSpikeAmplitudesData = (recordingObject, sortingObject) => {
    const hither = useContext(HitherContext);
    const fetch = useMemo(() => ((query) => __awaiter(void 0, void 0, void 0, function* () {
        switch (query.type) {
            case 'spikeAmplitudes': {
                return yield fetchSpikeAmplitudes({ hither, recordingObject, sortingObject, unitId: query.unitId });
            }
            default: throw Error('Unexpected query type');
        }
    })), [hither, recordingObject, sortingObject]);
    const data = useFetchCache(fetch);
    const getSpikeAmplitudes = useMemo(() => ((unitId) => {
        return data.get({ type: 'spikeAmplitudes', unitId });
    }), [data]);
    return useMemo(() => ({
        getSpikeAmplitudes
    }), [getSpikeAmplitudes]);
};
export default useSpikeAmplitudesData;
//# sourceMappingURL=useSpikeAmplitudesData.js.map