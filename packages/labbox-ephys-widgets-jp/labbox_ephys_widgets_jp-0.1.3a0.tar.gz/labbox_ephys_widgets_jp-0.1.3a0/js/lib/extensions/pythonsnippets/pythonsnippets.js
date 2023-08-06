// LABBOX-EXTENSION: pythonsnippets
// LABBOX-EXTENSION-TAGS:
import SubjectIcon from '@material-ui/icons/Subject';
import React from 'react';
import LoadSortingPythonSnippet from './LoadSortingPythonSnippet/LoadSortingPythonSnippet';
export function activate(context) {
    context.registerPlugin({
        type: 'SortingView',
        name: 'LoadSortingInPython',
        label: 'Load sorting in Python',
        priority: 0,
        component: LoadSortingPythonSnippet,
        singleton: true,
        icon: React.createElement(SubjectIcon, null)
    });
}
//# sourceMappingURL=pythonsnippets.js.map