// LABBOX-EXTENSION: snippets
// LABBOX-EXTENSION-TAGS: jupyter
import SnippetsView from './SnippetsView/SnippetsView';
export function activate(context) {
    context.registerPlugin({
        type: 'SortingView',
        name: 'SnippetsView',
        label: 'Snippets',
        priority: 50,
        component: SnippetsView
    });
}
//# sourceMappingURL=snippets.js.map