import { MenuItem, Select } from '@material-ui/core';
import React, { useCallback } from 'react';
import sizeMe from 'react-sizeme';
export const preprocessingSelectionReducer = (state, action) => {
    if (action.type === 'SetPreprocessingSelection') {
        return action.preprocessingSelection;
    }
    else {
        return state;
    }
};
const choices = [
    {
        preprocessingSelection: { filterType: 'none' },
        label: 'No filter'
    },
    {
        preprocessingSelection: { filterType: 'bandpass_filter' },
        label: 'Bandpass filter'
    }
];
const PreprocessingControl = ({ preprocessingSelection, preprocessingSelectionDispatch }) => {
    const handleChoice = useCallback((event) => {
        const preprocessingSelectionForValue = (val) => {
            return choices.filter(choice => (choice.preprocessingSelection.filterType === val))[0].preprocessingSelection;
        };
        preprocessingSelectionDispatch({ type: 'SetPreprocessingSelection', preprocessingSelection: preprocessingSelectionForValue(event.target.value) });
    }, [preprocessingSelectionDispatch]);
    return (React.createElement(Select, { value: preprocessingSelection.filterType, onChange: handleChoice }, choices.map(choice => (React.createElement(MenuItem, { key: choice.preprocessingSelection.filterType, value: choice.preprocessingSelection.filterType }, choice.label)))));
};
export default sizeMe()(PreprocessingControl);
//# sourceMappingURL=PreprocessingControl.js.map