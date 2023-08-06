import { FunctionComponent } from 'react';
import { View } from './MVSortingView';
declare type Props = {
    views: View[];
    currentView: View | null;
    onCurrentViewChanged: (v: View) => void;
    onViewClosed: (v: View) => void;
    active: boolean;
};
declare const ViewContainerTabBar: FunctionComponent<Props>;
export default ViewContainerTabBar;
