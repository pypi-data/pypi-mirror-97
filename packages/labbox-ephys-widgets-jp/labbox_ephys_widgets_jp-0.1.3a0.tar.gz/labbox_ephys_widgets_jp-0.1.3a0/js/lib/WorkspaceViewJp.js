var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
import { DOMWidgetModel, DOMWidgetView } from '@jupyter-widgets/base';
import { createExtensionContext, LabboxProvider } from 'labbox';
import React, { Suspense } from 'react';
import ReactDOM from 'react-dom';
import registerExtensions from './registerExtensions';
export class WorkspaceViewJp extends DOMWidgetView {
    constructor() {
        super(...arguments);
        // _hitherJobManager: HitherJobManager
        this._status = { active: true };
    }
    initialize() {
        // this._hitherJobManager = new HitherJobManager(this.model)
    }
    element() {
        return __awaiter(this, void 0, void 0, function* () {
            const workspaceUri = this.model.get('workspaceUri');
            const WorkspaceViewWrapper = React.lazy(() => import('./WorkspaceViewWrapper'));
            const extensionContext = createExtensionContext();
            yield registerExtensions(extensionContext);
            const apiConfig = {
                webSocketUrl: '',
                baseSha1Url: `/sha1`,
                baseFeedUrl: `/feed`,
                jupyterMode: true,
                jupyterModel: this.model
            };
            return (React.createElement(Suspense, { fallback: React.createElement("div", null, "Importing workspace view") },
                React.createElement(LabboxProvider, { extensionContext: extensionContext, apiConfig: apiConfig, status: this._status },
                    React.createElement(WorkspaceViewWrapper, { workspaceUri: workspaceUri }))));
        });
    }
    render() {
        this.element().then((reactElement) => {
            const widgetHeight = 700;
            this.el.classList.add('WorkspaceViewJp');
            renderJpWidget(this, reactElement, widgetHeight);
        });
    }
    remove() {
        this._status.active = false;
    }
}
const renderJpWidget = (W, reactElement, widgetHeight) => {
    const style = W.el.style;
    style.height = '100%';
    style['min-height'] = `${widgetHeight}px`;
    ReactDOM.render(reactElement, W.el);
};
export class WorkspaceViewJpModel extends DOMWidgetModel {
    initialize(attributes, options) {
        super.initialize(attributes, options);
    }
    defaults() {
        return Object.assign(Object.assign({}, super.defaults()), { _model_name: WorkspaceViewJpModel.model_name, _model_module: WorkspaceViewJpModel.model_module, _model_module_version: WorkspaceViewJpModel.model_module_version, _view_name: WorkspaceViewJpModel.view_name, _view_module: WorkspaceViewJpModel.view_module, _view_module_version: WorkspaceViewJpModel.view_module_version, workspaceUri: '' });
    }
}
WorkspaceViewJpModel.serializers = Object.assign({}, DOMWidgetModel.serializers);
WorkspaceViewJpModel.model_name = 'WorkspaceViewJpModel';
WorkspaceViewJpModel.model_module = 'labbox-ephys-widgets-jp';
WorkspaceViewJpModel.model_module_version = '0.1.3';
WorkspaceViewJpModel.view_name = 'WorkspaceViewJp'; // Set to null if no view
WorkspaceViewJpModel.view_module = 'labbox-ephys-widgets-jp'; // Set to null if no view
WorkspaceViewJpModel.view_module_version = '0.1.3';
//# sourceMappingURL=WorkspaceViewJp.js.map