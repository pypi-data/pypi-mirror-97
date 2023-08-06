import React from 'react';
const PeakChannels = (record) => {
    return (React.createElement("span", null, record !== undefined ? record : ''));
};
const plugin = {
    type: 'SortingUnitMetric',
    name: 'PeakChannels',
    label: 'Peak chan.',
    columnLabel: 'Peak chan.',
    tooltip: 'ID of channel where the peak-to-peak amplitude is maximal',
    hitherFnName: 'createjob_get_peak_channels',
    metricFnParams: {},
    hitherOpts: {
        useClientCache: true
    },
    component: PeakChannels,
    isNumeric: true,
    getValue: (record) => record
};
export default plugin;
//# sourceMappingURL=PeakChannels.js.map