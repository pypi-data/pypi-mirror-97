import { recordingSelectionReducer } from "./RecordingSelection";
import { isMergeGroupRepresentative } from "./SortingCuration";
const unitClickedReducer = (state, action) => {
    const unitId = action.unitId;
    if (action.ctrlKey) {
        if ((state.selectedUnitIds || []).includes(unitId)) {
            return Object.assign(Object.assign({}, state), { selectedUnitIds: (state.selectedUnitIds || []).filter(uid => (uid !== unitId)) });
        }
        else {
            return Object.assign(Object.assign({}, state), { selectedUnitIds: [...(state.selectedUnitIds || []), unitId] });
        }
    }
    // todo: restore anchor/shift-select behavior somewhere
    else {
        return Object.assign(Object.assign({}, state), { selectedUnitIds: [unitId] });
    }
};
export const sortingSelectionReducer = (state, action) => {
    if (action.type === 'SetSelection') {
        return action.selection;
    }
    else if (action.type === 'SetSelectedUnitIds') {
        return Object.assign(Object.assign({}, state), { selectedUnitIds: action.selectedUnitIds.filter(uid => { var _a; return ((!state.visibleUnitIds) || ((_a = state.visibleUnitIds) === null || _a === void 0 ? void 0 : _a.includes(uid))); }) });
    }
    else if (action.type === 'SetVisibleUnitIds') {
        return Object.assign(Object.assign({}, state), { selectedUnitIds: state.selectedUnitIds ? state.selectedUnitIds.filter(uid => { var _a; return (_a = action.visibleUnitIds) === null || _a === void 0 ? void 0 : _a.includes(uid); }) : undefined, visibleUnitIds: action.visibleUnitIds });
    }
    else if (action.type === 'UnitClicked') {
        return unitClickedReducer(state, action);
    }
    else if (action.type === 'Set') {
        return action.state;
    }
    else if (action.type === 'ToggleApplyMerges') {
        return adjustSelectedUnitIdsBasedOnMerges(Object.assign(Object.assign({}, state), { applyMerges: state.applyMerges ? false : true }), action.curation);
    }
    else {
        return recordingSelectionReducer(state, action);
    }
};
const adjustSelectedUnitIdsBasedOnMerges = (state, curation) => {
    return (state.applyMerges && curation) ? (Object.assign(Object.assign({}, state), { selectedUnitIds: state.selectedUnitIds ? state.selectedUnitIds.filter(uid => (isMergeGroupRepresentative(uid, curation))) : undefined })) : state;
};
//# sourceMappingURL=SortingSelection.js.map