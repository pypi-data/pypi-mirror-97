import React from 'react';
import sizeMe from 'react-sizeme';
declare const _default: React.ComponentType<{
    recording: import("../../pluginInterface").Recording;
    sorting: import("../../pluginInterface").Sorting;
    height: number;
    width: number;
    readOnly: boolean | null;
    curationDispatch?: ((action: import("../../pluginInterface/workspaceReducer").SortingCurationWorkspaceAction) => void) | undefined;
    selection: import("../../pluginInterface").SortingSelection;
    selectionDispatch: (a: import("../../pluginInterface").SortingSelectionAction) => void;
    sortingInfo: import("../../pluginInterface").SortingInfo;
    recordingInfo: import("../../pluginInterface").RecordingInfo;
    calculationPool: import("labbox").CalculationPool;
} & sizeMe.WithSizeProps>;
export default _default;
