export const externalUnitMetricsReducer = (state, action) => {
    if (action.type === 'SetExternalUnitMetrics') {
        return action.externalUnitMetrics;
    }
    else
        return state;
};
//# sourceMappingURL=exteneralUnitMetrics.js.map