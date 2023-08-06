var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
import { useEffect, useRef } from "react";
const TIME_ZOOM_FACTOR = 1.4;
const AMP_SCALE_FACTOR = 1.4;
export const useRecordingAnimation = (selection, selectionDispatch) => {
    const ref = useRef({
        lastUpdateTimestamp: Number(new Date()),
        selection,
        selectionDispatch
    });
    ref.current.selection = selection;
    ref.current.selectionDispatch = selectionDispatch;
    const animationFrame = () => {
        var _a;
        const lastUpdate = ref.current.lastUpdateTimestamp;
        const current = Number(new Date());
        const elapsed = current - lastUpdate;
        if (elapsed !== 0) {
            const currentTimepointVelocity = ((_a = ref.current.selection.animation) === null || _a === void 0 ? void 0 : _a.currentTimepointVelocity) || 0;
            const currentTimepoint = ref.current.selection.currentTimepoint;
            if ((currentTimepointVelocity) && (currentTimepoint !== undefined)) {
                const t = Math.round(currentTimepoint + currentTimepointVelocity * (elapsed / 1000));
                ref.current.selectionDispatch({ type: 'SetCurrentTimepoint', currentTimepoint: t });
            }
        }
        ref.current.lastUpdateTimestamp = Number(new Date());
    };
    // only do this once
    useEffect(() => {
        ;
        (() => __awaiter(void 0, void 0, void 0, function* () {
            while (true) {
                yield sleepMsec(50);
                animationFrame();
            }
        }))();
    }, []);
};
export const sleepMsec = (m) => new Promise(r => setTimeout(r, m));
const adjustTimeRangeToIncludeTimepoint = (timeRange, timepoint) => {
    if ((timeRange.min <= timepoint) && (timepoint < timeRange.max))
        return timeRange;
    const span = timeRange.max - timeRange.min;
    const t1 = Math.max(0, Math.floor(timepoint - span / 2));
    const t2 = t1 + span;
    return { min: t1, max: t2 };
};
export const recordingSelectionReducer = (state, action) => {
    var _a, _b, _c, _d;
    if (action.type === 'SetRecordingSelection') {
        return Object.assign({}, action.recordingSelection);
    }
    else if (action.type === 'SetSelectedElectrodeIds') {
        return Object.assign(Object.assign({}, state), { selectedElectrodeIds: action.selectedElectrodeIds.filter(eid => ((!state.visibleElectrodeIds) || (state.visibleElectrodeIds.includes(eid)))) });
    }
    else if (action.type === 'SetVisibleElectrodeIds') {
        return Object.assign(Object.assign({}, state), { visibleElectrodeIds: action.visibleElectrodeIds, selectedElectrodeIds: state.selectedElectrodeIds ? state.selectedElectrodeIds.filter(eid => (action.visibleElectrodeIds.includes(eid))) : undefined });
    }
    else if (action.type === 'SetCurrentTimepoint') {
        return Object.assign(Object.assign({}, state), { currentTimepoint: action.currentTimepoint || undefined, timeRange: action.ensureInRange && (state.timeRange) && (action.currentTimepoint !== null) ? adjustTimeRangeToIncludeTimepoint(state.timeRange, action.currentTimepoint) : state.timeRange });
    }
    else if (action.type === 'SetTimeRange') {
        return Object.assign(Object.assign({}, state), { timeRange: action.timeRange });
    }
    else if (action.type === 'ZoomTimeRange') {
        const maxTimeSpan = 30000 * 60 * 5;
        const currentTimepoint = state.currentTimepoint;
        const timeRange = state.timeRange;
        if (!timeRange)
            return state;
        const direction = (_a = action.direction) !== null && _a !== void 0 ? _a : 'in';
        const pre_factor = (_b = action.factor) !== null && _b !== void 0 ? _b : TIME_ZOOM_FACTOR;
        const factor = direction === 'out' ? 1 / pre_factor : pre_factor;
        if ((timeRange.max - timeRange.min) / factor > maxTimeSpan)
            return state;
        let t;
        if ((currentTimepoint === undefined) || (currentTimepoint < timeRange.min))
            t = timeRange.min;
        else if (currentTimepoint > timeRange.max)
            t = timeRange.max;
        else
            t = currentTimepoint;
        const newTimeRange = zoomTimeRange(timeRange, factor, t);
        return Object.assign(Object.assign({}, state), { timeRange: newTimeRange });
        // return fix({
        //     ...state,
        //     timeRange: newTimeRange
        // })
    }
    else if (action.type === 'SetAmpScaleFactor') {
        return Object.assign(Object.assign({}, state), { ampScaleFactor: action.ampScaleFactor });
    }
    else if (action.type === 'ScaleAmpScaleFactor') {
        const direction = (_c = action.direction) !== null && _c !== void 0 ? _c : 'up';
        const pre_multiplier = (_d = action.multiplier) !== null && _d !== void 0 ? _d : AMP_SCALE_FACTOR;
        const multiplier = direction === 'down' ? 1 / pre_multiplier : pre_multiplier;
        return Object.assign(Object.assign({}, state), { ampScaleFactor: (state.ampScaleFactor || 1) * multiplier });
    }
    else if (action.type === 'SetCurrentTimepointVelocity') {
        return Object.assign(Object.assign({}, state), { animation: Object.assign(Object.assign({}, (state.animation || {})), { currentTimepointVelocity: action.velocity }) });
    }
    else if (action.type === 'SetWaveformsMode') {
        return Object.assign(Object.assign({}, state), { waveformsMode: action.waveformsMode });
    }
    else if (action.type === 'Set') {
        return action.state;
    }
    else
        return state;
};
const zoomTimeRange = (timeRange, factor, anchorTime) => {
    const oldT1 = timeRange.min;
    const oldT2 = timeRange.max;
    const t1 = anchorTime + (oldT1 - anchorTime) / factor;
    const t2 = anchorTime + (oldT2 - anchorTime) / factor;
    return { min: Math.floor(t1), max: Math.floor(t2) };
};
//# sourceMappingURL=RecordingSelection.js.map