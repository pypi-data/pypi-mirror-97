export const mergeGroupForUnitId = (unitId, curation) => {
    const mergeGroups = (curation || {}).mergeGroups || [];
    return mergeGroups.filter(g => (g.includes(unitId)))[0] || null;
};
export const applyMergesToUnit = (unitId, curation, applyMerges) => {
    return applyMerges ? (mergeGroupForUnitId(unitId, curation) || unitId) : unitId;
};
export const isMergeGroupRepresentative = (unitId, curation) => {
    const mg = mergeGroupForUnitId(unitId, curation);
    if (!mg)
        return true;
    return (Math.min(...mg) === unitId);
};
//# sourceMappingURL=SortingCuration.js.map