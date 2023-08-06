var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
import { HitherContext, useHitherJob } from 'labbox';
import { useContext, useRef, useState } from "react";
export const getRecordingInfo = (a) => __awaiter(void 0, void 0, void 0, function* () {
    const recordingInfoJob = a.hither.createHitherJob('createjob_get_recording_info', { recording_object: a.recordingObject }, {
        useClientCache: true
    });
    const info = yield recordingInfoJob.wait();
    return info;
});
export const useRecordingInfo = (recordingObject) => {
    const { result: recordingInfo } = useHitherJob(recordingObject ? 'createjob_get_recording_info' : '', { recording_object: recordingObject }, { useClientCache: true });
    return recordingInfo;
};
export const useRecordingInfos = (recordings) => {
    const hither = useContext(HitherContext);
    const jobs = useRef({});
    const [, setCount] = useState(0); // just for triggering update
    const ret = {};
    recordings.forEach(r => {
        const rid = r.recordingId;
        if (!jobs.current[rid]) {
            const j = hither.createHitherJob('createjob_get_recording_info', { recording_object: r.recordingObject }, { useClientCache: true });
            jobs.current[rid] = j;
            j.wait().then(() => {
                setCount(c => (c + 1));
            })
                .catch(() => {
                setCount(c => (c + 1));
            });
        }
        if (jobs.current[rid].result) {
            ret[rid] = jobs.current[rid].result;
        }
    });
    return ret;
};
//# sourceMappingURL=useRecordingInfo.js.map