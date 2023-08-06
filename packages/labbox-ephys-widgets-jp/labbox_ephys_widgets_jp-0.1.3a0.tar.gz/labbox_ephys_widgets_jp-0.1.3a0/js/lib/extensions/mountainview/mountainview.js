// LABBOX-EXTENSION: mountainview
// LABBOX-EXTENSION-TAGS: jupyter
import MVSortingUnitView from './MVSortingUnitView/MVSortingUnitView';
import MVSortingView from './MVSortingView/MVSortingView';
export function activate(context) {
    context.registerPlugin({
        type: 'SortingView',
        name: 'MVSortingView',
        label: 'MVSortingView',
        priority: 5000,
        defaultExpanded: true,
        notebookCellHeight: 800,
        component: MVSortingView
    });
    context.registerPlugin({
        type: 'SortingUnitView',
        name: 'MVSortingUnitView',
        label: 'MV sorting unit view',
        component: MVSortingUnitView
    });
}
//# sourceMappingURL=mountainview.js.map