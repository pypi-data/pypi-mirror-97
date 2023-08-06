import { Checkbox, IconButton, Table, TableBody, TableCell, TableHead, TableRow } from '@material-ui/core';
import { Delete, Edit } from "@material-ui/icons";
import React, { useCallback, useMemo, useState } from 'react';
import './NiceTable.css';
const NiceTable = ({ rows, columns, onDeleteRow = undefined, deleteRowLabel = undefined, onEditRow = undefined, editRowLabel = undefined, selectionMode = 'none', // none, single, multiple
selectedRowKeys = {}, onSelectedRowKeysChanged = undefined }) => {
    const selectedRowKeysObj = useMemo(() => {
        const x = {};
        Object.keys(selectedRowKeys).forEach((key) => { x[key] = selectedRowKeys[key]; });
        return x;
    }, [selectedRowKeys]);
    const [confirmDeleteRowKey, setConfirmDeleteRowKey] = useState(null);
    const handleClickRow = useCallback((key) => {
        if (!onSelectedRowKeysChanged || false)
            return;
        if (selectionMode === 'single') {
            if (!(key in selectedRowKeysObj) || !selectedRowKeysObj[key]) {
                onSelectedRowKeysChanged([key + '']);
            }
            else {
                onSelectedRowKeysChanged([]);
            }
        }
        else if (selectionMode === 'multiple') {
            // todo: write this logic. Note, we'll need to also pass in the event to get the ctrl/shift modifiers
            onSelectedRowKeysChanged(Object.keys(selectedRowKeysObj)
                // eslint-disable-next-line eqeqeq
                .filter(k => k != key && selectedRowKeysObj[k])
                .concat(selectedRowKeysObj[key] ? [] : [key.toString()]));
        }
    }, [onSelectedRowKeysChanged, selectionMode, selectedRowKeysObj]);
    const handleDeleteRow = useCallback((rowKey) => {
        setConfirmDeleteRowKey(rowKey);
    }, []);
    const handleConfirmDeleteRow = useCallback((rowKey, confirmed) => {
        if (confirmed) {
            onDeleteRow && onDeleteRow(rowKey);
        }
        setConfirmDeleteRowKey(null);
    }, [onDeleteRow]);
    const handleEditRow = useCallback((rowKey) => {
        onEditRow && onEditRow(rowKey);
    }, [onEditRow]);
    return (React.createElement(Table, { className: "NiceTable" },
        React.createElement(TableHead, null,
            React.createElement(TableRow, null,
                React.createElement(TableCell, { key: "_first", style: { width: 0 } }),
                columns.map(col => (React.createElement(TableCell, { key: col.key },
                    React.createElement("span", null, col.label)))))),
        React.createElement(TableBody, null, rows.map(row => (React.createElement(TableRow, { key: row.key },
            React.createElement(TableCell, null,
                onDeleteRow && ((confirmDeleteRowKey === row.key) ? (React.createElement(ConfirmDeleteRowButton, { title: deleteRowLabel || '', onConfirmDeleteRow: handleConfirmDeleteRow, rowKey: row.key })) : ((React.createElement(DeleteRowButton, { title: deleteRowLabel || '', onDeleteRow: handleDeleteRow, rowKey: row.key })))),
                onEditRow && (React.createElement(EditRowButton, { title: editRowLabel || '', onEditRow: handleEditRow, rowKey: row.key })),
                selectionMode !== 'none' && (React.createElement(Checkbox, { checked: selectedRowKeysObj[row.key] || false, onClick: () => handleClickRow(row.key) }))),
            columns.map(col => (React.createElement(TableCell, { key: col.key },
                React.createElement("span", null, makeCell(row.columnValues[col.key])))))))))));
};
const DeleteRowButton = ({ title, rowKey, onDeleteRow }) => {
    const handleClick = useCallback(() => {
        onDeleteRow && onDeleteRow(rowKey);
    }, [onDeleteRow, rowKey]);
    return (React.createElement(IconButton, { title: title, onClick: handleClick },
        React.createElement(Delete, null)));
};
const ConfirmDeleteRowButton = ({ title, rowKey, onConfirmDeleteRow }) => {
    const handleClick = useCallback(() => {
        onConfirmDeleteRow && onConfirmDeleteRow(rowKey, true);
    }, [onConfirmDeleteRow, rowKey]);
    const handleCancel = useCallback(() => {
        onConfirmDeleteRow && onConfirmDeleteRow(rowKey, false);
    }, [onConfirmDeleteRow, rowKey]);
    return (React.createElement("span", null,
        "Confirm delete?",
        React.createElement(IconButton, { title: title, onClick: handleClick },
            React.createElement(Delete, null)),
        React.createElement(IconButton, { title: "Cancel", onClick: handleCancel }, "\u2716")));
};
const EditRowButton = ({ title, rowKey, onEditRow }) => {
    return (React.createElement(IconButton, { title: title, onClick: () => onEditRow && onEditRow(rowKey) },
        React.createElement(Edit, null)));
};
const makeCell = (x) => {
    // eslint-disable-next-line eqeqeq
    if (x == 0)
        return x; // !'0' is true, but we shouldn't null out actual 0s
    if (!x)
        return '';
    if (typeof (x) == "object") {
        if (x.element)
            return x.element;
        else
            return x.text || '';
    }
    else {
        return x;
    }
};
export default NiceTable;
//# sourceMappingURL=NiceTable.js.map