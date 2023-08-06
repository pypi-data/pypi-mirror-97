import { FunctionComponent } from 'react';
import { View } from './MVSortingView';
declare type Props = {
    views: View[];
    onViewClosed: (v: View) => void;
    onSetViewArea: (v: View, area: 'north' | 'south') => void;
    width: number;
    height: number;
};
declare const ViewContainer: FunctionComponent<Props>;
export default ViewContainer;
