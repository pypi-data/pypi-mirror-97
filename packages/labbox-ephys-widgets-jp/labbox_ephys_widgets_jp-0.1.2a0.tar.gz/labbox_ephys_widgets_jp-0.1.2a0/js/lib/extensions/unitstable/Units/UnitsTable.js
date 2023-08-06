import React, { useCallback } from 'react';
import { mergeGroupForUnitId } from "../../pluginInterface";
import sortByPriority from '../../sortByPriority';
import '../unitstable.css';
import TableWidget from './TableWidget';
const UnitsTable = (props) => {
    const { sortingUnitMetrics, units, metrics, selection, selectionDispatch, sorting, height } = props;
    const selectedUnitIds = ((selection || {}).selectedUnitIds || []);
    const sortingUnitMetricsList = sortByPriority(Object.values(sortingUnitMetrics || {})).filter(p => (!p.disabled));
    const handleSelectedRowIdsChanged = useCallback((selectedRowIds) => {
        selectionDispatch({
            type: 'SetSelectedUnitIds',
            selectedUnitIds: selectedRowIds.map(id => Number(id))
        });
    }, [selectionDispatch]);
    const rows = units.map(unitId => ({
        rowId: unitId + '',
        data: {}
    }));
    const numericSort = (a, b) => {
        return (Number(a) - Number(b));
    };
    const numericElement = (x) => (React.createElement("span", null, x + ''));
    const unitIdStyle = {
        color: 'black',
        fontWeight: 'bold',
        cursor: 'pointer'
    };
    const unitIdElement = (x) => {
        const { unitId, mergeGroup } = x;
        return (React.createElement("span", null,
            React.createElement("span", { key: "unitId", style: unitIdStyle }, unitId + ''),
            ((mergeGroup) && (mergeGroup.length > 0)) && (React.createElement("span", { key: "mergeGroup" }, ` (${mergeGroup.map(id => (id + '')).join(", ")})`))));
    };
    const alphaSort = (a, b) => {
        return (a < b) ? -1 : (a > b) ? 1 : 0;
    };
    const labelStyle = {
        color: 'gray',
        textDecoration: 'underline',
        cursor: 'pointer'
    };
    const labelsElement = (x) => {
        const y = x;
        return (React.createElement("span", null, y.map(label => (React.createElement("span", { key: label },
            React.createElement("span", { style: labelStyle }, label),
            "\u00A0")))));
    };
    const columns = [];
    // first column (Unit ID)
    columns.push({
        columnName: '_unit_id',
        label: 'Unit ID',
        tooltip: 'Unit ID',
        sort: numericSort,
        dataElement: unitIdElement
    });
    rows.forEach(row => {
        const unitId = Number(row.rowId);
        row.data['_unit_id'] = {
            value: { unitId, mergeGroup: mergeGroupForUnitId(unitId, sorting.curation) },
            sortValue: unitId
        };
    });
    // second column (Labels)
    columns.push({
        columnName: '_labels',
        label: 'Labels',
        tooltip: 'Curation labels',
        sort: alphaSort,
        dataElement: labelsElement
    });
    rows.forEach(row => {
        const unitId = Number(row.rowId);
        const labels = getLabelsForUnitId(unitId, sorting);
        row.data['_labels'] = {
            value: labels,
            sortValue: labels.join(', ')
        };
    });
    (sorting.externalUnitMetrics || []).forEach((m) => {
        const columnName = 'external-metric-' + m.name;
        columns.push({
            columnName,
            label: m.label,
            tooltip: m.tooltip || '',
            sort: numericSort,
            dataElement: numericElement
        });
        rows.forEach(row => {
            const unitId = Number(row.rowId);
            const v = m.data[unitId + ''];
            row.data[columnName] = {
                value: v !== undefined ? v : NaN,
                sortValue: v !== undefined ? v : NaN
            };
        });
    });
    (sortingUnitMetricsList).forEach((m) => {
        const columnName = 'plugin-metric-' + m.name;
        const metric = (metrics || {})[m.name] || null;
        const metricData = metric ? metric.data : null;
        columns.push({
            columnName,
            label: m.columnLabel,
            tooltip: m.tooltip || '',
            sort: numericSort,
            dataElement: m.component,
            calculating: (metric && (!metricData))
        });
        rows.forEach(row => {
            const unitId = Number(row.rowId);
            const record = metricData ? ((unitId + '' in metricData) ? metricData[unitId + ''] : undefined) : undefined;
            const v = (record !== undefined) ? m.getValue(record) : undefined;
            row.data[columnName] = {
                value: record,
                sortValue: v !== undefined ? v : (m.isNumeric ? NaN : '')
            };
        });
    });
    const selectedRowIds = selectedUnitIds.map(unitId => (unitId + ''));
    return (React.createElement(TableWidget, { rows: rows, columns: columns, selectedRowIds: selectedRowIds, onSelectedRowIdsChanged: handleSelectedRowIdsChanged, defaultSortColumnName: "_unit_id", height: height }));
};
const getLabelsForUnitId = (unitId, sorting) => {
    const labelsByUnit = (sorting.curation || {}).labelsByUnit || {};
    return labelsByUnit[unitId] || [];
};
// const UnitIdCell = React.memo((props: {id: number, mergeGroup: number[] | null, sortingId: string}) => {
//     const g = props.mergeGroup
//     return <TableCell><span>{props.id + ''}{g && ' (' + [...g].sort().join(', ') + ')'}</span></TableCell>
// })
// const UnitLabelCell = React.memo((props: {labels: string}) => (
//     <TableCell><span>{props.labels}</span></TableCell>
// ));
// const MetricCell = React.memo((a: {title?: string, error: string, data: any, PayloadComponent: React.ComponentType<{record: any}>}) => {
//     const { error, data, PayloadComponent } = a
//     if (error !== '') {
//         return (<TableCell><span>{`Error: ${error}`}</span></TableCell>);
//     }
//     if (data === null || data === '') { // 0 is a valid value!!
//         return (<TableCell><LinearProgress style={{'width': '60%'}}/></TableCell>);
//     } else {
//         return (
//             <TableCell>
//                 <span title={a.title}>
//                     <PayloadComponent record = {data} />
//                 </span>
//             </TableCell>
//         );
//     }
// });
export default UnitsTable;
//# sourceMappingURL=UnitsTable.js.map