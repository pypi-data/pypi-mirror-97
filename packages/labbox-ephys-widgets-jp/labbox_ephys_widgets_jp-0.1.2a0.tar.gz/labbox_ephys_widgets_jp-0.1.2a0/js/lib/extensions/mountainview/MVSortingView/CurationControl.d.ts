import React from 'react';
import sizeMe from 'react-sizeme';
import { SortingCuration, SortingSelection, SortingSelectionDispatch } from '../../pluginInterface';
import { SortingCurationWorkspaceAction } from '../../pluginInterface/workspaceReducer';
declare const _default: React.ComponentType<{
    curationDispatch: (a: SortingCurationWorkspaceAction) => void;
    selection: SortingSelection;
    selectionDispatch: SortingSelectionDispatch;
    sortingId: string;
    curation: SortingCuration;
} & sizeMe.WithSizeProps>;
export default _default;
