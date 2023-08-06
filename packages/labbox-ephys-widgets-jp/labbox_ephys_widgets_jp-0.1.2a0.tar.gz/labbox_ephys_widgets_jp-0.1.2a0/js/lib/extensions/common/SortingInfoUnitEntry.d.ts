import React, { FunctionComponent } from 'react';
import './localStyles.css';
interface Props {
    unitId: number;
    labels: string;
    unitStatus: 'unselected' | 'selected';
    onUnitClicked: (unitId: number, event: React.MouseEvent<HTMLDivElement, MouseEvent>) => void;
}
declare const SortingInfoUnitEntry: FunctionComponent<Props>;
export default SortingInfoUnitEntry;
