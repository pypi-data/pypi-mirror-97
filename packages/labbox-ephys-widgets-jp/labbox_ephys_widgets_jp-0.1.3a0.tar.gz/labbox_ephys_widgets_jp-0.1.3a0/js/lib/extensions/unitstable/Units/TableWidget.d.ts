import { FunctionComponent } from 'react';
import '../unitstable.css';
export interface Row {
    rowId: string;
    data: {
        [key: string]: {
            value: any;
            sortValue: any;
        };
    };
}
export interface Column {
    columnName: string;
    label: string;
    tooltip: string;
    sort: (a: any, b: any) => number;
    dataElement: (d: any) => JSX.Element;
    calculating?: boolean;
}
interface Props {
    selectedRowIds: string[];
    onSelectedRowIdsChanged: (x: string[]) => void;
    rows: Row[];
    columns: Column[];
    defaultSortColumnName?: string;
    height?: number;
}
declare const TableWidget: FunctionComponent<Props>;
export default TableWidget;
