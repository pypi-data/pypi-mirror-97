import { createCalculationPool, useHitherJob } from 'labbox';
import React, { useCallback, useMemo } from 'react';
import HitherJobStatusView from '../../common/HitherJobStatusView';
import { applyMergesToUnit } from "../../pluginInterface";
import IndividualClusterWidget from './IndividualClusterWidget';
const calculationPool = createCalculationPool({ maxSimultaneous: 6 });
const IndividualClusterView = ({ recording, sorting, selection, selectionDispatch, unitId, width, height }) => {
    const { result: features, job } = useHitherJob('createjob_individual_cluster_features', {
        recording_object: recording.recordingObject,
        sorting_object: sorting.sortingObject,
        unit_id: applyMergesToUnit(unitId, sorting.curation, selection.applyMerges)
    }, {
        useClientCache: true,
        calculationPool
    });
    const selectedIndex = useMemo(() => {
        const t = selection.currentTimepoint;
        if (t === undefined)
            return undefined;
        if (features === undefined)
            return undefined;
        for (let i = 0; i < features.timepoints.length; i++) {
            if (Math.abs(features.timepoints[i] - t) < 20) {
                return i;
            }
        }
    }, [features, selection]);
    const handleSelectedIndexChanged = useCallback((i) => {
        if (i === undefined)
            return;
        if (features === undefined)
            return;
        const t = features.timepoints[i];
        if (t === undefined)
            return;
        selectionDispatch({ type: 'SetCurrentTimepoint', currentTimepoint: t, ensureInRange: true });
    }, [features, selectionDispatch]);
    if (!features) {
        return React.createElement(HitherJobStatusView, Object.assign({}, { job, width, height }));
    }
    return (React.createElement(IndividualClusterWidget, Object.assign({ x: features.x, y: features.y }, { width, height, selectedIndex }, { onSelectedIndexChanged: handleSelectedIndexChanged })));
};
export default IndividualClusterView;
//# sourceMappingURL=IndividualClusterView.js.map