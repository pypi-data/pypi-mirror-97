import { Paper } from "@material-ui/core";
import React from 'react';
import SortingsTable from './SortingsTable';
const SortingsView = ({ sortings, workspaceRouteDispatch, workspaceRoute, onDeleteSortings }) => {
    return (React.createElement(Paper, null,
        React.createElement("h3", null, `${sortings.length} sortings`),
        React.createElement(SortingsTable, { sortings: sortings, workspaceRouteDispatch: workspaceRouteDispatch, readOnly: false, onDeleteSortings: onDeleteSortings })));
};
export default SortingsView;
//# sourceMappingURL=SortingsView.js.map