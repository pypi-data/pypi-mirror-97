import React from 'react';
const EventCount = (record) => {
    return (React.createElement("span", null, record !== undefined ? record.count : ''));
};
const plugin = {
    type: 'SortingUnitMetric',
    name: 'EventCount',
    label: 'Num. events',
    columnLabel: 'Num. events',
    tooltip: 'Number of firing events',
    hitherFnName: 'createjob_get_firing_data',
    metricFnParams: {},
    hitherOpts: {
        useClientCache: true
    },
    component: EventCount,
    isNumeric: true,
    getValue: (record) => record.count
};
export default plugin;
//# sourceMappingURL=EventCount.js.map