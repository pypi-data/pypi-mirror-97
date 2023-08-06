import { Checkbox, Grid, Paper } from '@material-ui/core';
import React, { useCallback, useMemo } from 'react';
import sizeMe from 'react-sizeme';
const buttonStyle = {
    paddingTop: 3, paddingBottom: 3, border: 1, borderStyle: 'solid', borderColor: 'gray'
};
const CurationControl = ({ sortingId, selection, selectionDispatch, curation, curationDispatch, size }) => {
    const width = size.width || 300;
    const selectedUnitIds = useMemo(() => (selection.selectedUnitIds || []), [selection.selectedUnitIds]);
    const _handleApplyLabel = useCallback((label) => {
        for (let unitId of selectedUnitIds) {
            curationDispatch({
                type: 'ADD_UNIT_LABEL',
                sortingId: sortingId,
                unitId,
                label
            });
        }
    }, [curationDispatch, selectedUnitIds, sortingId]);
    const _handleRemoveLabel = useCallback((label) => {
        for (let unitId of selectedUnitIds) {
            curationDispatch({
                type: 'REMOVE_UNIT_LABEL',
                sortingId,
                unitId,
                label
            });
        }
    }, [curationDispatch, selectedUnitIds, sortingId]);
    const handleMergeSelected = useCallback(() => {
        curationDispatch({
            type: 'MERGE_UNITS',
            sortingId,
            unitIds: selectedUnitIds
        });
    }, [curationDispatch, selectedUnitIds, sortingId]);
    const handleUnmergeSelected = useCallback(() => {
        curationDispatch({
            type: 'UNMERGE_UNITS',
            sortingId,
            unitIds: selectedUnitIds
        });
    }, [curationDispatch, selectedUnitIds, sortingId]);
    const handleToggleApplyMerges = useCallback(() => {
        selectionDispatch({ type: 'ToggleApplyMerges', curation });
    }, [selectionDispatch, curation]);
    const labelCounts = {};
    for (const uid of selectedUnitIds) {
        const labels = (curation.labelsByUnit || {})[uid + ''] || [];
        for (const label of labels) {
            let c = labelCounts[label] || 0;
            c++;
            labelCounts[label] = c;
        }
    }
    const labels = Object.keys(labelCounts).sort();
    const labelRecords = labels.map(label => ({
        label,
        partial: labelCounts[label] < selectedUnitIds.length ? true : false
    }));
    const paperStyle = {
        marginTop: 25,
        marginBottom: 25,
        backgroundColor: '#f9f9ff'
    };
    const unitsAreInMergeGroups = (unitIds) => {
        const mg = curation.mergeGroups || [];
        const all = mg.reduce((prev, g) => [...prev, ...g], []); // all units in merge groups
        for (let unitId of unitIds) {
            if (!all.includes(unitId))
                return false;
        }
        return true;
    };
    const enableApply = selectedUnitIds.length > 0;
    const standardChoices = ['accept', 'reject', 'noise', 'artifact', 'mua'];
    const labelChoices = [...standardChoices, ...(curation.labelChoices || []).filter(l => (!standardChoices.includes(l)))];
    return (React.createElement("div", { style: { width, position: 'relative' } },
        React.createElement(Paper, { style: paperStyle, key: "selected" },
            "Selected units: ",
            selectedUnitIds.join(', ')),
        React.createElement(Paper, { style: paperStyle, key: "labels" },
            "Labels:",
            React.createElement(Grid, { container: true, style: { flexFlow: 'wrap' }, spacing: 0 }, labelRecords.map(r => (React.createElement(Grid, { item: true, key: r.label },
                React.createElement(Label, { label: r.label, partial: r.partial, onClick: () => { r.partial ? _handleApplyLabel(r.label) : _handleRemoveLabel(r.label); } })))))),
        React.createElement(Paper, { style: paperStyle, key: "apply" },
            "Apply labels:",
            React.createElement(Grid, { container: true, style: { flexFlow: 'wrap' }, spacing: 0 }, labelChoices.map(labelChoice => (React.createElement(Grid, { item: true, key: labelChoice }, (((labelCounts[labelChoice] || 0) < selectedUnitIds.length) || (!enableApply)) ? (React.createElement("button", { style: buttonStyle, disabled: !enableApply, onClick: () => { _handleApplyLabel(labelChoice); } }, labelChoice)) : React.createElement("span", null)))))),
        React.createElement(Paper, { style: paperStyle, key: "merge" },
            "Merge:",
            selectedUnitIds.length >= 2 && React.createElement("button", { key: "merge", onClick: handleMergeSelected },
                "Merge selected units: ",
                selectedUnitIds.join(', ')),
            (selectedUnitIds.length > 0 && unitsAreInMergeGroups(selectedUnitIds)) && React.createElement("button", { key: "unmerge", onClick: handleUnmergeSelected },
                "Unmerge units: ",
                selectedUnitIds.join(', ')),
            React.createElement("span", { style: { whiteSpace: 'nowrap' } },
                React.createElement(Checkbox, { checked: selection.applyMerges || false, onClick: handleToggleApplyMerges }),
                " Apply merges"))));
};
const Label = ({ label, partial, onClick }) => {
    const color = partial ? 'gray' : 'black';
    return (React.createElement("button", { style: Object.assign(Object.assign({}, buttonStyle), { color }), onClick: onClick }, label));
};
export default sizeMe()(CurationControl);
//# sourceMappingURL=CurationControl.js.map