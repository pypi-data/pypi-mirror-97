import React from 'react';
const UnitSnrs = (record) => {
    return (React.createElement("span", null, record !== undefined ? record.toFixed(4) : ''));
};
const plugin = {
    type: 'SortingUnitMetric',
    name: 'UnitSnrs',
    label: 'SNR',
    columnLabel: 'SNR',
    tooltip: 'Unit SNR (peak-to-peak amp of mean waveform / est. std. dev on peak chan)',
    hitherFnName: 'createjob_get_unit_snrs',
    metricFnParams: {},
    hitherOpts: {
        useClientCache: true
    },
    component: UnitSnrs,
    isNumeric: true,
    getValue: (record) => record
};
export default plugin;
//# sourceMappingURL=UnitSnrs.js.map