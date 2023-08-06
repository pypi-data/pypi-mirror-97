import { Button } from '@material-ui/core';
import React, { useCallback, useState } from 'react';
import Splitter from '../../common/Splitter';
import ImportRecordingsInstructions from './ImportRecordingsInstructions';
import RecordingsTable from './RecordingsTable';
const WorkspaceRecordingsView = ({ width, height, sortings, recordings, onDeleteRecordings, workspaceRoute, workspaceRouteDispatch }) => {
    const [showImportInstructions, setShowImportInstructions] = useState(false);
    const handleImport = useCallback(() => {
        setShowImportInstructions(true);
    }, []);
    return (React.createElement(Splitter, Object.assign({}, { width, height }, { initialPosition: 300, positionFromRight: true }),
        React.createElement("div", null,
            !showImportInstructions && (React.createElement("div", null,
                React.createElement(Button, { onClick: handleImport }, "Import recordings"))),
            React.createElement(RecordingsTable, Object.assign({}, { sortings, recordings, onDeleteRecordings, readOnly: false, workspaceRouteDispatch }))),
        showImportInstructions && (React.createElement(ImportRecordingsInstructions, { workspaceRoute: workspaceRoute }))));
};
export default WorkspaceRecordingsView;
//# sourceMappingURL=WorkspaceRecordingsView.js.map