import React from 'react';
const IsiViolations = (record) => {
    return (React.createElement("span", null, record !== undefined ? record.toFixed(4) : ''));
};
const plugin = {
    type: 'SortingUnitMetric',
    name: 'IsiViolations',
    label: 'ISI viol.',
    columnLabel: 'ISI viol.',
    tooltip: 'ISI violation rate',
    hitherFnName: 'createjob_get_isi_violation_rates',
    metricFnParams: {
        'isi_threshold_msec': 2.5
        // need to sort out how to pass unit ids list?
    },
    hitherOpts: {
        useClientCache: true
    },
    component: IsiViolations,
    isNumeric: true,
    getValue: (record) => record
};
export default plugin;
//# sourceMappingURL=IsiViolations.js.map