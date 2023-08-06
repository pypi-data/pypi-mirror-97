// LABBOX-EXTENSION: correlograms
// LABBOX-EXTENSION-TAGS: jupyter
import BarChartIcon from '@material-ui/icons/BarChart';
import React from 'react';
import AutoCorrelograms from "./AutoCorrelograms";
import CrossCorrelogramsView from "./CrossCorrelogramsView/CrossCorrelogramsView";
export function activate(context) {
    context.registerPlugin({
        type: 'SortingView',
        name: 'Autocorrelograms',
        label: 'Autocorrelograms',
        priority: 50,
        component: AutoCorrelograms,
        icon: React.createElement(BarChartIcon, null),
        singleton: true
    });
    context.registerPlugin({
        type: 'SortingView',
        name: 'CrossCorrelograms',
        label: 'Cross-Correlograms',
        component: CrossCorrelogramsView,
        icon: React.createElement(BarChartIcon, null),
        singleton: false
    });
}
//# sourceMappingURL=correlograms.js.map