import { faPencilAlt } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { GraphicEq, Settings, Visibility } from '@material-ui/icons';
import GrainIcon from '@material-ui/icons/Grain';
import OpenInBrowserIcon from '@material-ui/icons/OpenInBrowser';
import { usePlugins } from 'labbox';
import React, { useCallback, useEffect, useMemo, useReducer, useState } from 'react';
import Expandable from '../../common/Expandable';
import Splitter from '../../common/Splitter';
import { sortingViewPlugins } from "../../pluginInterface";
import '../mountainview.css';
import CurationControl from './CurationControl';
import OptionsControl from './OptionsControl';
import PreloadCheck from './PreloadCheck';
import PreprocessingControl, { preprocessingSelectionReducer } from './PreprocessingControl';
import ViewContainer from './ViewContainer';
import ViewLauncher from './ViewLauncher';
import ViewWidget from './ViewWidget';
import VisibleElectrodesControl from './VisibleElectrodesControl';
import VisibleUnitsControl from './VisibleUnitsControl';
const initialLeftPanelWidth = 320;
export class View {
    constructor(plugin, extraProps, label, viewId) {
        this.plugin = plugin;
        this.extraProps = extraProps;
        this.label = label;
        this.viewId = viewId;
        this.activate = false; // signal to set this tab as active
        this.area = '';
    }
}
let lastViewIdNum = 0;
export const openViewsReducer = (state, action) => {
    if (action.type === 'AddView') {
        const plugin = action.plugin;
        if (plugin.singleton) {
            for (let v0 of state) {
                if (v0.plugin.name === plugin.name) {
                    v0.activate = true;
                    return [...state];
                }
            }
        }
        lastViewIdNum++;
        const v = new View(plugin, action.extraProps || {}, action.label, lastViewIdNum + '');
        v.activate = true; // signal to set this as active
        v.area = action.area;
        return [...state, v].sort((a, b) => (a.plugin.label > b.plugin.label ? 1 : a.plugin.label < b.plugin.label ? -1 : 0));
    }
    else if (action.type === 'CloseView') {
        return state.filter(v => (v !== action.view));
    }
    else if (action.type === 'SetViewArea') {
        return state.map(v => (v.viewId === action.viewId ? Object.assign(Object.assign({}, v), { area: action.area, activate: true }) : v));
    }
    else
        return state;
};
const area = (a) => {
    return a;
};
const MVSortingViewWithCheck = (props) => {
    const { recording, sorting } = props;
    const [preprocessingSelection, preprocessingSelectionDispatch] = useReducer(preprocessingSelectionReducer, { filterType: 'none' });
    const preprocessedRecording = useMemo(() => {
        if (!recording)
            return recording;
        if (preprocessingSelection.filterType === 'none') {
            return recording;
        }
        else if (preprocessingSelection.filterType === 'bandpass_filter') {
            return Object.assign(Object.assign({}, recording), { recordingObject: {
                    recording_format: 'filtered',
                    data: {
                        filters: [{ type: 'bandpass_filter', freq_min: 300, freq_max: 3000, freq_wid: 1000 }],
                        recording: recording.recordingObject
                    }
                } });
        }
        else {
            throw Error(`Unexpected filter type: ${preprocessingSelection.filterType}`);
        }
    }, [recording, preprocessingSelection]);
    return (React.createElement(PreloadCheck, { recording: preprocessedRecording, sorting: sorting, width: props.width || 0, height: props.height || 0 },
        React.createElement(MVSortingView, Object.assign({}, props, { preprocessingSelection, preprocessingSelectionDispatch }, { recording: preprocessedRecording }))));
};
const MVSortingView = (props) => {
    // useCheckForChanges('MVSortingView', props)
    const { recording, sorting, recordingInfo, selection, selectionDispatch, preloadStatus, preprocessingSelection, preprocessingSelectionDispatch, curationDispatch } = props;
    const [openViews, openViewsDispatch] = useReducer(openViewsReducer, []);
    const [initializedViews, setInitializedViews] = useState(false);
    const plugins = usePlugins();
    const UnitsTablePlugin = sortingViewPlugins(plugins).filter(p => (p.name === 'UnitsTable'))[0];
    const AverageWaveformsPlugin = sortingViewPlugins(plugins).filter(p => (p.name === 'AverageWaveforms'))[0];
    const initialPluginViews = useMemo(() => ([
        { plugin: UnitsTablePlugin, area: area('north') },
        { plugin: AverageWaveformsPlugin, area: area('south') }
    ]).filter(x => (x.plugin !== undefined)), [UnitsTablePlugin, AverageWaveformsPlugin]);
    // const electrodeGeometryPlugin = plugins.sortingViews.ElectrodeGeometrySortingView
    useEffect(() => {
        if ((preloadStatus === 'finished') && (openViews.length === 0) && (!initializedViews)) {
            setInitializedViews(true);
            initialPluginViews.forEach(x => {
                // openViewsDispatch({
                //     type: 'AddView',
                //     plugin: x.plugin,
                //     pluginType: 'SortingView',
                //     label: x.plugin.label,
                //     area: x.area
                // })
            });
        }
    }, [preloadStatus, initializedViews, initialPluginViews, openViews.length]);
    const handleLaunchSortingView = useCallback((plugin) => {
        openViewsDispatch({
            type: 'AddView',
            plugin,
            label: plugin.label,
            area: ''
        });
    }, [openViewsDispatch]);
    const handleLaunchSortingUnitView = useCallback((plugin, unitId, label) => {
        openViewsDispatch({
            type: 'AddView',
            plugin,
            label,
            area: '',
            extraProps: { unitId }
        });
    }, [openViewsDispatch]);
    const handleViewClosed = useCallback((v) => {
        openViewsDispatch({
            type: 'CloseView',
            view: v
        });
    }, [openViewsDispatch]);
    const handleSetViewArea = useCallback((view, area) => {
        openViewsDispatch({
            type: 'SetViewArea',
            viewId: view.viewId,
            area
        });
    }, [openViewsDispatch]);
    const width = props.width || 600;
    const height = props.height || 900;
    const preprocessingIcon = React.createElement("span", { style: { color: 'gray' } },
        React.createElement(GraphicEq, null));
    const visibleUnitsIcon = React.createElement("span", { style: { color: 'gray' } },
        React.createElement(Visibility, null));
    const visibleElectrodesIcon = React.createElement("span", { style: { color: 'gray' } },
        React.createElement(GrainIcon, null));
    const launchIcon = React.createElement("span", { style: { color: 'gray' } },
        React.createElement(OpenInBrowserIcon, null));
    const curationIcon = React.createElement("span", { style: { color: 'gray' } },
        React.createElement(FontAwesomeIcon, { icon: faPencilAlt }));
    const optionsIcon = React.createElement("span", { style: { color: 'gray' } },
        React.createElement(Settings, null));
    const sortingViewProps = Object.assign({}, props);
    return (React.createElement("div", { className: "MVSortingView" },
        React.createElement(Splitter, { width: width, height: height, initialPosition: initialLeftPanelWidth },
            React.createElement("div", null,
                React.createElement(Expandable, { icon: launchIcon, label: "Open views", defaultExpanded: true, unmountOnExit: false },
                    React.createElement(ViewLauncher, { onLaunchSortingView: handleLaunchSortingView, onLaunchSortingUnitView: handleLaunchSortingUnitView, selection: props.selection })),
                React.createElement(Expandable, { icon: visibleUnitsIcon, label: "Visible units", defaultExpanded: false, unmountOnExit: false },
                    React.createElement(VisibleUnitsControl, { sorting: sorting, recording: recording, selection: selection, selectionDispatch: selectionDispatch })),
                React.createElement(Expandable, { icon: visibleElectrodesIcon, label: "Visible electrodes", defaultExpanded: false, unmountOnExit: false },
                    React.createElement(VisibleElectrodesControl, { recordingInfo: recordingInfo, selection: selection, selectionDispatch: selectionDispatch })),
                React.createElement(Expandable, { icon: preprocessingIcon, label: "Preprocessing", defaultExpanded: false, unmountOnExit: false },
                    React.createElement(PreprocessingControl, { preprocessingSelection: preprocessingSelection, preprocessingSelectionDispatch: preprocessingSelectionDispatch })),
                curationDispatch && (React.createElement(Expandable, { icon: curationIcon, label: "Curation", defaultExpanded: false, unmountOnExit: false },
                    React.createElement(CurationControl, { sortingId: sorting.sortingId, curation: props.sorting.curation || {}, curationDispatch: curationDispatch, selection: props.selection, selectionDispatch: props.selectionDispatch }))),
                React.createElement(Expandable, { icon: optionsIcon, label: "Options", defaultExpanded: false, unmountOnExit: false },
                    React.createElement(OptionsControl, { selection: selection, selectionDispatch: selectionDispatch }))),
            React.createElement(ViewContainer, { onViewClosed: handleViewClosed, onSetViewArea: handleSetViewArea, views: openViews, width: 0, height: 0 }, openViews.map(v => (React.createElement(ViewWidget, { key: v.viewId, view: v, sortingViewProps: sortingViewProps })))))));
};
export default MVSortingViewWithCheck;
//# sourceMappingURL=MVSortingView.js.map