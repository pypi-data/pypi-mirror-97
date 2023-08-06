// LABBOX-EXTENSION: spikeamplitudes
// LABBOX-EXTENSION-TAGS: jupyter
import ScatterPlotIcon from '@material-ui/icons/ScatterPlot';
import React from 'react';
import SpikeAmplitudesUnitView from './SpikeAmplitudesView/SpikeAmplitudesUnitView';
import SpikeAmplitudesView from './SpikeAmplitudesView/SpikeAmplitudesView';
export function activate(context) {
    context.registerPlugin({
        type: 'SortingView',
        name: 'SpikeAmplitudes',
        label: 'Spike amplitudes',
        priority: 50,
        defaultExpanded: false,
        component: SpikeAmplitudesView,
        singleton: false,
        icon: React.createElement(ScatterPlotIcon, null)
    });
    context.registerPlugin({
        type: 'SortingUnitView',
        name: 'SpikeAmplitudes',
        label: 'Spike amplitudes',
        priority: 50,
        fullWidth: true,
        component: SpikeAmplitudesUnitView,
        icon: React.createElement(ScatterPlotIcon, null)
    });
}
//# sourceMappingURL=spikeamplitudes.js.map