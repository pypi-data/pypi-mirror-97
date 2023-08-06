import React from 'react';
import sizeMe from 'react-sizeme';
export declare type PreprocessingSelection = {
    filterType: 'none' | 'bandpass_filter';
};
export declare type PreprocessingSelectionAction = {
    type: 'SetPreprocessingSelection';
    preprocessingSelection: PreprocessingSelection;
};
export declare const preprocessingSelectionReducer: (state: PreprocessingSelection, action: PreprocessingSelectionAction) => PreprocessingSelection;
declare const _default: React.ComponentType<{
    preprocessingSelection: PreprocessingSelection;
    preprocessingSelectionDispatch: (a: PreprocessingSelectionAction) => void;
} & sizeMe.WithSizeProps>;
export default _default;
