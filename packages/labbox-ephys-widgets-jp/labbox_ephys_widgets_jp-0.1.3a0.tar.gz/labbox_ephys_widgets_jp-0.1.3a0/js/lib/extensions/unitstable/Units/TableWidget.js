import { faCaretDown, faCaretUp } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { Checkbox, Grid, LinearProgress, Table, TableBody, TableCell, TableContainer, TableHead, TableRow } from '@material-ui/core';
import React, { useCallback, useEffect, useState } from 'react';
import '../unitstable.css';
const HeaderRow = (props) => {
    const { columns, onColumnClick, primarySortColumnDirection, primarySortColumnName, onDeselectAll } = props;
    return (React.createElement(TableHead, null,
        React.createElement(TableRow, null,
            onDeselectAll ? (React.createElement(TableCell, { key: "_checkbox" },
                React.createElement(RowCheckbox, { rowId: '', selected: false, onClick: () => { onDeselectAll(); }, isDeselectAll: true }))) : (React.createElement(TableCell, { key: "_checkbox" })),
            columns.map(column => {
                const tooltip = (column.tooltip || column.label || '') + ' (click to sort)';
                return (React.createElement(TableCell, { key: column.columnName, onClick: () => onColumnClick(column), title: tooltip, style: { cursor: 'pointer' } },
                    React.createElement(Grid, { container: true, justify: "flex-start", style: { flexFlow: 'row' } },
                        React.createElement(Grid, { item: true, key: "icon" },
                            React.createElement("span", { style: { fontSize: 16, color: 'gray', paddingLeft: 3, paddingRight: 5, paddingTop: 2 } }, (primarySortColumnName === column.columnName) && (primarySortColumnDirection === 'ascending' ? (
                            // <TriangleUp fontSize="inherit" />
                            React.createElement(FontAwesomeIcon, { icon: faCaretUp })) : (React.createElement(FontAwesomeIcon, { icon: faCaretDown }))))),
                        React.createElement(Grid, { item: true, key: "text" },
                            React.createElement("span", null,
                                React.createElement("span", { key: "label" }, column.label),
                                React.createElement("span", { key: "progress" }, column.calculating && React.createElement(LinearProgress, null)))))));
            }))));
};
const RowCheckbox = React.memo((props) => {
    const { rowId, selected, onClick, isDeselectAll } = props;
    return (React.createElement(Checkbox, { checked: selected, indeterminate: isDeselectAll ? true : false, onClick: () => onClick(rowId), style: {
            padding: 1
        }, title: isDeselectAll ? "Deselect all" : `Select ${rowId}` }));
});
const interpretSortFields = (fields) => {
    const result = [];
    for (let i = 0; i < fields.length; i++) {
        // We are ascending unless two fields in a row are the same
        const sortAscending = (fields[i - 1] !== fields[i]);
        result.push({ columnName: fields[i], keyOrder: i, sortAscending });
    }
    return result;
};
const TableWidget = (props) => {
    const { selectedRowIds, onSelectedRowIdsChanged, rows, columns, defaultSortColumnName, height } = props;
    const [sortFieldOrder, setSortFieldOrder] = useState([]);
    useEffect(() => {
        if ((sortFieldOrder.length === 0) && (defaultSortColumnName)) {
            setSortFieldOrder([defaultSortColumnName]);
        }
    }, [setSortFieldOrder, sortFieldOrder, defaultSortColumnName]);
    const toggleSelectedRowId = useCallback((rowId) => {
        const newSelectedRowIds = selectedRowIds.includes(rowId) ? selectedRowIds.filter(x => (x !== rowId)) : [...selectedRowIds, rowId];
        onSelectedRowIdsChanged(newSelectedRowIds);
    }, [selectedRowIds, onSelectedRowIdsChanged]);
    const sortedRows = [...rows];
    const columnForName = (columnName) => (columns.filter(c => (c.columnName === columnName))[0]);
    const sortingRules = interpretSortFields(sortFieldOrder);
    for (const r of sortingRules) {
        const columnName = r.columnName;
        const column = columnForName(columnName);
        sortedRows.sort((a, b) => {
            const dA = (a.data[columnName] || {});
            const dB = (b.data[columnName] || {});
            const valueA = dA.sortValue;
            const valueB = dB.sortValue;
            return r.sortAscending ? column.sort(valueA, valueB) : column.sort(valueB, valueA);
        });
    }
    const selectedRowIdsLookup = (selectedRowIds || []).reduce((m, id) => { m[id] = true; return m; }, {});
    const primaryRule = (sortingRules.length > 0) ? sortingRules[sortingRules.length - 1] : undefined;
    const primarySortColumnName = primaryRule ? primaryRule.columnName : undefined;
    const primarySortColumnDirection = primaryRule ? (primaryRule.sortAscending ? 'ascending' : 'descending') : undefined;
    return (React.createElement(TableContainer, { style: height !== undefined ? { maxHeight: height } : {} },
        React.createElement(Table, { stickyHeader: true, className: "TableWidget" },
            React.createElement(HeaderRow, { columns: columns, primarySortColumnName: primarySortColumnName, primarySortColumnDirection: primarySortColumnDirection, onColumnClick: (column) => {
                    const columnName = column.columnName;
                    let newSortFieldOrder = [...sortFieldOrder];
                    if (sortFieldOrder[sortFieldOrder.length - 1] === columnName) {
                        if (sortFieldOrder[sortFieldOrder.length - 2] === columnName) {
                            // the last two match this column, let's just remove the last one
                            newSortFieldOrder = newSortFieldOrder.slice(0, newSortFieldOrder.length - 1);
                        }
                        else {
                            // the last one matches this column, let's add another one
                            newSortFieldOrder = [...newSortFieldOrder, columnName];
                        }
                    }
                    else {
                        // the last one does not match this column, let's clear out all previous instances and add one
                        newSortFieldOrder = [...newSortFieldOrder.filter(m => (m !== columnName)), columnName];
                    }
                    setSortFieldOrder(newSortFieldOrder);
                }, onDeselectAll: selectedRowIds.length > 0 ? () => { onSelectedRowIdsChanged([]); } : undefined }),
            React.createElement(TableBody, null, sortedRows.map((row) => {
                const selected = selectedRowIdsLookup[row.rowId] || false;
                return (React.createElement(TableRow, { key: row.rowId },
                    React.createElement(TableCell, { key: "_checkbox", className: selected ? "selectedRow" : "" },
                        React.createElement(RowCheckbox, { rowId: row.rowId, selected: selected, onClick: () => toggleSelectedRowId(row.rowId) })),
                    columns.map(column => (React.createElement(TableCell, { key: column.columnName, className: selected ? "selectedRow" : "" },
                        React.createElement("div", { title: column.tooltip }, column.dataElement(row.data[column.columnName].value)))))));
            })))));
};
export default TableWidget;
//# sourceMappingURL=TableWidget.js.map