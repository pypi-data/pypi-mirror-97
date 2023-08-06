// This file was automatically generated. Do not edit directly.
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
const registerExtensions = (context) => __awaiter(void 0, void 0, void 0, function* () {
    const { activate: activate_mainwindow } = yield import('./extensions/mainwindow/mainwindow');
    activate_mainwindow(context);
    const { activate: activate_workspaceview } = yield import('./extensions/workspaceview/workspaceview');
    activate_workspaceview(context);
    const { activate: activate_mountainview } = yield import('./extensions/mountainview/mountainview');
    activate_mountainview(context);
    const { activate: activate_averagewaveforms } = yield import('./extensions/averagewaveforms/averagewaveforms');
    activate_averagewaveforms(context);
    const { activate: activate_clusters } = yield import('./extensions/clusters/clusters');
    activate_clusters(context);
    const { activate: activate_correlograms } = yield import('./extensions/correlograms/correlograms');
    activate_correlograms(context);
    const { activate: activate_electrodegeometry } = yield import('./extensions/electrodegeometry/electrodegeometry');
    activate_electrodegeometry(context);
    const { activate: activate_firetrack } = yield import('./extensions/firetrack/firetrack');
    activate_firetrack(context);
    const { activate: activate_pythonsnippets } = yield import('./extensions/pythonsnippets/pythonsnippets');
    activate_pythonsnippets(context);
    const { activate: activate_snippets } = yield import('./extensions/snippets/snippets');
    activate_snippets(context);
    const { activate: activate_spikeamplitudes } = yield import('./extensions/spikeamplitudes/spikeamplitudes');
    activate_spikeamplitudes(context);
    const { activate: activate_timeseries } = yield import('./extensions/timeseries/timeseries');
    activate_timeseries(context);
    const { activate: activate_unitstable } = yield import('./extensions/unitstable/unitstable');
    activate_unitstable(context);
});
export default registerExtensions;
//# sourceMappingURL=registerExtensions.js.map