/// <reference types="react" />
import { DOMWidgetModel, DOMWidgetView, ISerializers } from '@jupyter-widgets/base';
export declare class WorkspaceViewJp extends DOMWidgetView {
    _status: {
        active: boolean;
    };
    initialize(): void;
    element(): Promise<JSX.Element>;
    render(): void;
    remove(): void;
}
export declare class WorkspaceViewJpModel extends DOMWidgetModel {
    initialize(attributes: any, options: any): void;
    defaults(): any;
    static serializers: ISerializers;
    static model_name: string;
    static model_module: string;
    static model_module_version: string;
    static view_name: string;
    static view_module: string;
    static view_module_version: string;
}
