// LABBOX-EXTENSION: clusters
// LABBOX-EXTENSION-TAGS: jupyter
import { BubbleChart } from '@material-ui/icons';
import React from 'react';
import IndividualClustersView from './IndividualClustersView/IndividualClustersView';
export function activate(context) {
    context.registerPlugin({
        type: 'SortingView',
        name: 'IndividualClustersView',
        label: 'Clusters',
        priority: 50,
        component: IndividualClustersView,
        icon: React.createElement(BubbleChart, null)
    });
}
//# sourceMappingURL=clusters.js.map