import React from 'react';
const FiringRate = (record) => {
    return (React.createElement("span", null, record !== undefined ? record.rate : ''));
};
const plugin = {
    type: 'SortingUnitMetric',
    name: 'FiringRate',
    label: 'Firing rate (Hz)',
    columnLabel: 'Firing rate (Hz)',
    tooltip: 'Average num. events per second',
    hitherFnName: 'createjob_get_firing_data',
    hitherOpts: {
        useClientCache: true
    },
    metricFnParams: {},
    component: FiringRate,
    isNumeric: true,
    getValue: (record) => record.count
};
export default plugin;
//# sourceMappingURL=FiringRate.js.map