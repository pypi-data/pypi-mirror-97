import { Table, TableCell, TableRow } from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';
import { LabboxProviderContext } from 'labbox';
import React, { useContext } from 'react';
import { parseWorkspaceUri } from '../../pluginInterface/misc';
const useStyles = makeStyles((theme) => ({
    paper: {
        left: 100,
        top: 100,
        right: 100,
        bottom: 100,
        position: 'absolute',
        backgroundColor: theme.palette.background.paper,
        border: '2px solid #000',
        boxShadow: theme.shadows[5],
        padding: theme.spacing(2, 4, 3),
        overflow: 'auto'
    },
}));
const SettingsWindow = ({ workspaceUri }) => {
    const classes = useStyles();
    const { serverInfo } = useContext(LabboxProviderContext);
    const { workspaceName } = parseWorkspaceUri(workspaceUri);
    return (React.createElement("div", { className: classes.paper, style: { zIndex: 9999 } },
        React.createElement("h2", null, "Labbox Ephys 0.5.4"),
        React.createElement(Table, null,
            React.createElement(TableRow, null,
                React.createElement(TableCell, null, "Workspace URI"),
                React.createElement(TableCell, null, workspaceUri || '')),
            React.createElement(TableRow, null,
                React.createElement(TableCell, null, "Workspace name"),
                React.createElement(TableCell, null, workspaceName)),
            React.createElement(TableRow, null,
                React.createElement(TableCell, null, "Kachery node ID"),
                React.createElement(TableCell, null, serverInfo ? serverInfo.nodeId : '')),
            React.createElement(TableRow, null,
                React.createElement(TableCell, null, "Default feed ID"),
                React.createElement(TableCell, null, serverInfo ? serverInfo.defaultFeedId : '')))));
};
export default SettingsWindow;
//# sourceMappingURL=SettingsWindow.js.map