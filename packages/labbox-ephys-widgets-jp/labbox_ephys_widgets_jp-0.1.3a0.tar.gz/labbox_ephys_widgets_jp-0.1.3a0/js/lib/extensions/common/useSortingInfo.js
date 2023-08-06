import { HitherContext, useHitherJob } from 'labbox';
import { useContext, useRef, useState } from "react";
export const useSortingInfo = (sortingObject, recordingObject) => {
    const { result: sortingInfo } = useHitherJob(sortingObject ? 'createjob_get_sorting_info' : '', { sorting_object: sortingObject, recording_object: recordingObject }, { useClientCache: true });
    return sortingInfo;
};
export const useSortingInfos = (sortings) => {
    const hither = useContext(HitherContext);
    const jobs = useRef({});
    const [, setCount] = useState(0); // just for triggering update
    const ret = {};
    sortings.forEach(s => {
        const rid = s.sortingId;
        if (!jobs.current[rid]) {
            const j = hither.createHitherJob('createjob_get_sorting_info', { recording_object: s.recordingObject, sorting_object: s.sortingObject }, { useClientCache: true });
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
//# sourceMappingURL=useSortingInfo.js.map