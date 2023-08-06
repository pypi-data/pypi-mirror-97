import { CircularProgress } from '@material-ui/core';
import React, { useCallback, useMemo } from 'react';
import NiceTable from '../../common/NiceTable';
import { useSortingInfos } from '../../common/useSortingInfo';
const SortingsTable = ({ sortings, onDeleteSortings, readOnly, workspaceRouteDispatch }) => {
    const handleViewSorting = useCallback((sorting) => {
        workspaceRouteDispatch({
            type: 'gotoSortingPage',
            recordingId: sorting.recordingId,
            sortingId: sorting.sortingId
        });
    }, [workspaceRouteDispatch]);
    const sortingInfos = useSortingInfos(sortings);
    const sortings2 = useMemo(() => (sortByKey(sortings, 'sortingLabel')), [sortings]);
    const rows = useMemo(() => (sortings2.map(s => {
        const sortingInfo = sortingInfos[s.sortingId];
        return {
            key: s.sortingId,
            columnValues: {
                sorting: s,
                sortingLabel: {
                    text: s.sortingLabel,
                    element: React.createElement(ViewSortingLink, { sorting: s, onClick: handleViewSorting })
                },
                numUnits: sortingInfo ? sortingInfo.unit_ids.length : { element: React.createElement(CircularProgress, null) }
            }
        };
    })), [sortings2, handleViewSorting, sortingInfos]);
    const handleDeleteRow = useCallback((key) => {
        onDeleteSortings && onDeleteSortings([key]);
    }, [onDeleteSortings]);
    const columns = [
        {
            key: 'sortingLabel',
            label: 'Sorting'
        },
        {
            key: 'numUnits',
            label: 'Num. units'
        }
    ];
    return (React.createElement("div", null,
        React.createElement(NiceTable, { rows: rows, columns: columns, deleteRowLabel: "Remove this sorting", onDeleteRow: readOnly ? undefined : handleDeleteRow })));
};
const ViewSortingLink = ({ sorting, onClick }) => {
    const handleClick = useCallback(() => {
        onClick(sorting);
    }, [sorting, onClick]);
    return (React.createElement(Anchor, { title: "View recording", onClick: handleClick }, sorting.sortingLabel));
};
const Anchor = ({ title, children, onClick }) => {
    return (React.createElement("button", { type: "button", className: "link-button", onClick: onClick }, children));
};
const sortByKey = (array, key) => {
    return array.sort(function (a, b) {
        var x = a[key];
        var y = b[key];
        return ((x < y) ? -1 : ((x > y) ? 1 : 0));
    });
};
export default SortingsTable;
//# sourceMappingURL=SortingsTable.js.map