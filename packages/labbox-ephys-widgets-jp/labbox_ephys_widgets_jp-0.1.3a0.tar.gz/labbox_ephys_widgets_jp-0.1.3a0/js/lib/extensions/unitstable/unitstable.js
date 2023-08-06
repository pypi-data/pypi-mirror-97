// LABBOX-EXTENSION: unitstable
// LABBOX-EXTENSION-TAGS: jupyter
import TableChartIcon from '@material-ui/icons/TableChart';
import React from 'react';
import registerMetricPlugins from "./Units/metricPlugins/registerMetricPlugins";
import Units from './Units/Units';
export function activate(context) {
    registerMetricPlugins(context);
    context.registerPlugin({
        type: 'SortingView',
        name: 'UnitsTable',
        label: 'Units Table',
        icon: React.createElement(TableChartIcon, null),
        priority: 200,
        component: Units,
        props: {
            maxHeight: 300
        },
        singleton: true
    });
}
//# sourceMappingURL=unitstable.js.map