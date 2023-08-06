import React, { FunctionComponent } from 'react';
import { SortingUnitViewPlugin, SortingViewPlugin, SortingViewProps } from "../../pluginInterface";
import { RecordingViewPlugin } from '../../pluginInterface/RecordingViewPlugin';
import '../mountainview.css';
declare type ViewPlugin = SortingViewPlugin | RecordingViewPlugin | SortingUnitViewPlugin;
declare type AddViewAction = {
    type: 'AddView';
    plugin: ViewPlugin;
    label: string;
    area: 'north' | 'south' | '';
    extraProps?: {
        [key: string]: any;
    };
};
declare type CloseViewAction = {
    type: 'CloseView';
    view: View;
};
declare type SetViewAreaAction = {
    type: 'SetViewArea';
    viewId: string;
    area: 'north' | 'south';
};
export declare class View {
    plugin: ViewPlugin;
    extraProps: {
        [key: string]: any;
    };
    label: string;
    viewId: string;
    activate: boolean;
    area: 'north' | 'south' | '';
    constructor(plugin: ViewPlugin, extraProps: {
        [key: string]: any;
    }, label: string, viewId: string);
}
declare type OpenViewsAction = AddViewAction | CloseViewAction | SetViewAreaAction;
export declare const openViewsReducer: React.Reducer<View[], OpenViewsAction>;
declare const MVSortingViewWithCheck: FunctionComponent<SortingViewProps>;
export default MVSortingViewWithCheck;
