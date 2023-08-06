import { IJupyterWidgetRegistry } from '@jupyter-widgets/base';
declare const labPlugin: {
    id: string;
    requires: import("@lumino/coreutils").Token<IJupyterWidgetRegistry>[];
    activate: (app: any, widgets: any) => void;
    autoStart: boolean;
};
export default labPlugin;
