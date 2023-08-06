import { FunctionComponent } from 'react';
declare type Props = {
    x: number[];
    y: number[];
    width: number;
    height: number;
    selectedIndex?: number;
    onSelectedIndexChanged?: (i: number | undefined) => void;
};
declare const IndividualClusterWidget: FunctionComponent<Props>;
export default IndividualClusterWidget;
