import { FunctionComponent } from 'react';
import { SortingViewProps } from "../../pluginInterface";
import { View } from './MVSortingView';
declare type Props = {
    view: View;
    sortingViewProps: SortingViewProps;
    width?: number;
    height?: number;
};
declare const ViewWidget: FunctionComponent<Props>;
export default ViewWidget;
