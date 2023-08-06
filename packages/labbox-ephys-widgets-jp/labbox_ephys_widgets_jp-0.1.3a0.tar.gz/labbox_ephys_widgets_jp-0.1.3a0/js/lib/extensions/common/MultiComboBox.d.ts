import React, { FunctionComponent } from 'react';
declare const MultiComboBox: FunctionComponent<{
    id: string;
    label: string;
    placeholder: string;
    onSelectionsChanged: (evt: React.ChangeEvent<{}>, value: any) => void;
    getLabelFromOption?: (option: any) => string;
    selectedOptionLabels?: string[];
    options?: string[];
}>;
export default MultiComboBox;
