import { FunctionComponent } from 'react';
import './NiceTable.css';
interface Row {
    key: string;
    columnValues: {
        [key: string]: any;
    };
}
interface Col {
    key: string;
    label: string;
}
interface Props {
    rows: Row[];
    columns: Col[];
    onDeleteRow?: (key: string) => void;
    deleteRowLabel?: string;
    onEditRow?: (key: string) => void;
    editRowLabel?: string;
    selectionMode?: 'none' | 'single' | 'multiple';
    selectedRowKeys?: {
        [key: string]: boolean;
    };
    onSelectedRowKeysChanged?: ((keys: string[]) => void);
}
declare const NiceTable: FunctionComponent<Props>;
export default NiceTable;
