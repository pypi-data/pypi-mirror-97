import React from 'react';
import Splitter from '../../common/Splitter';
import SelectUnitsWidget from '../../spikeamplitudes/SpikeAmplitudesView/SelectUnitsWidget';
import SnippetsWidget from './SnippetsWidget';
const SnippetsView = ({ recording, sorting, selection, selectionDispatch, width, height }) => {
    return (React.createElement(Splitter, { width: width || 600, height: height || 900, initialPosition: 200 },
        React.createElement(SelectUnitsWidget, { sorting: sorting, selection: selection, selectionDispatch: selectionDispatch }),
        React.createElement(SnippetsWidget, Object.assign({ recording: recording, sorting: sorting, selection: selection, selectionDispatch: selectionDispatch, unitIds: selection.selectedUnitIds || [] }, { width: 0, height: 0 }))));
};
export default SnippetsView;
//# sourceMappingURL=SnippetsView.js.map