import React, { useMemo, useState } from 'react';
import Splitter from '../../common/Splitter';
import SelectUnitsWidget from '../../spikeamplitudes/SpikeAmplitudesView/SelectUnitsWidget';
import CrossCorrelogramsWidget from './CrossCorrelogramsWidget';
const useLocalUnitIds = (selection, selectionDispatch) => {
    const [selectedUnitIds, setSelectedUnitIds] = useState([]);
    const selectionLocal = useMemo(() => (Object.assign(Object.assign({}, selection), { selectedUnitIds })), [selectedUnitIds, selection]);
    const selectionDispatchLocal = useMemo(() => ((action) => {
        if (action.type === 'SetSelectedUnitIds') {
            setSelectedUnitIds(action.selectedUnitIds);
        }
        else {
            selectionDispatch(action);
        }
    }), [selectionDispatch]);
    return [selectionLocal, selectionDispatchLocal];
};
const CrossCorrelogramsView = ({ sorting, selection, selectionDispatch, width, height }) => {
    // Make a local selection/selectionDispatch pair that overrides the selectedUnitIds
    const [selectionLocal, selectionDispatchLocal] = useLocalUnitIds(selection, selectionDispatch);
    return (React.createElement(Splitter, { width: width || 600, height: height || 900, initialPosition: 200 },
        React.createElement(SelectUnitsWidget, { sorting: sorting, selection: selectionLocal, selectionDispatch: selectionDispatchLocal }),
        React.createElement(CrossCorrelogramsWidget, Object.assign({ sorting: sorting, selection: selectionLocal, selectionDispatch: selectionDispatchLocal, unitIds: selectionLocal.selectedUnitIds || [] }, { width: 0, height: 0 }))));
};
export default CrossCorrelogramsView;
//# sourceMappingURL=CrossCorrelogramsView.js.map