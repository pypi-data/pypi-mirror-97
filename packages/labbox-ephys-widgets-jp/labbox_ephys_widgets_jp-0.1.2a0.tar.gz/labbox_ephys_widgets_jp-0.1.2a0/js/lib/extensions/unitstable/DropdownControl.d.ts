import React from 'react';
declare const DropdownControl: React.FunctionComponent<{
    label: string;
    value: any;
    onSetValue: (v: any) => void;
    options: {
        value: any;
        label: string;
    }[];
}>;
export default DropdownControl;
