export const sortingCurationReducer = (state, action) => {
    if (action.type === 'SET_CURATION') {
        return action.curation;
    }
    else if (action.type === 'ADD_UNIT_LABEL') {
        const uid = action.unitId + '';
        const labels = (state.labelsByUnit || {})[uid] || [];
        if (!labels.includes(action.label)) {
            return Object.assign(Object.assign({}, state), { labelsByUnit: Object.assign(Object.assign({}, state.labelsByUnit), { [uid]: [...labels, action.label].sort() }) });
        }
        else
            return state;
    }
    else if (action.type === 'REMOVE_UNIT_LABEL') {
        const uid = action.unitId + '';
        const labels = (state.labelsByUnit || {})[uid] || [];
        if (labels.includes(action.label)) {
            return Object.assign(Object.assign({}, state), { labelsByUnit: Object.assign(Object.assign({}, state.labelsByUnit), { [uid]: labels.filter(l => (l !== action.label)) }) });
        }
        else
            return state;
    }
    else if (action.type === 'MERGE_UNITS') {
        return Object.assign(Object.assign({}, state), { mergeGroups: simplifyMergeGroups([...(state.mergeGroups || []), action.unitIds]) });
    }
    else if (action.type === 'UNMERGE_UNITS') {
        return Object.assign(Object.assign({}, state), { mergeGroups: simplifyMergeGroups((state.mergeGroups || []).map(g => (g.filter(x => (!action.unitIds.includes(x)))))) });
    }
    else
        return state;
};
const workspaceReducer = (s, a) => {
    switch (a.type) {
        case 'ADD_RECORDING': return Object.assign(Object.assign({}, s), { recordings: [...s.recordings.filter(r => (r.recordingId !== a.recording.recordingId)), a.recording] });
        case 'DELETE_RECORDINGS': return Object.assign(Object.assign({}, s), { recordings: s.recordings.filter(x => !a.recordingIds.includes(x.recordingId)) });
        case 'ADD_SORTING': return Object.assign(Object.assign({}, s), { sortings: [...s.sortings.filter(x => (x.sortingId !== a.sorting.sortingId)), a.sorting] });
        case 'DELETE_SORTINGS': return Object.assign(Object.assign({}, s), { sortings: s.sortings.filter(x => !a.sortingIds.includes(x.sortingId)) });
        case 'DELETE_SORTINGS_FOR_RECORDINGS': return Object.assign(Object.assign({}, s), { sortings: s.sortings.filter(x => !a.recordingIds.includes(x.recordingId)) });
        case 'ADD_UNIT_LABEL':
        case 'REMOVE_UNIT_LABEL':
        case 'MERGE_UNITS':
        case 'UNMERGE_UNITS':
            return Object.assign(Object.assign({}, s), { sortings: s.sortings.map(x => (x.sortingId === a.sortingId) ? Object.assign(Object.assign({}, x), { curation: sortingCurationReducer(x.curation || {}, a) }) : x) });
        default: return s;
    }
};
const intersection = (a, b) => (a.filter(x => (b.includes(x))));
const union = (a, b) => ([...a, ...b.filter(x => (!a.includes(x)))].sort());
const simplifyMergeGroups = (mg) => {
    const newMergeGroups = mg.map(g => [...g]); // make a copy
    let somethingChanged = true;
    while (somethingChanged) {
        somethingChanged = false;
        for (let i = 0; i < newMergeGroups.length; i++) {
            const g1 = newMergeGroups[i];
            for (let j = i + 1; j < newMergeGroups.length; j++) {
                const g2 = newMergeGroups[j];
                if (intersection(g1, g2).length > 0) {
                    newMergeGroups[i] = union(g1, g2);
                    newMergeGroups[j] = [];
                    somethingChanged = true;
                }
            }
        }
    }
    return newMergeGroups.filter(g => (g.length >= 2));
};
export default workspaceReducer;
//# sourceMappingURL=workspaceReducer.js.map