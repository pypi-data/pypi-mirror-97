import { usePlugins } from 'labbox';
import React, { Fragment, useCallback } from 'react';
import { sortingUnitViewPlugins, sortingViewPlugins } from "../../pluginInterface";
import sortByPriority from '../../sortByPriority';
const buttonStyle = {
    fontSize: 12,
    padding: 4,
    margin: 1
};
const ViewLauncher = ({ onLaunchSortingView, onLaunchSortingUnitView, selection }) => {
    const plugins = usePlugins();
    const sortingUnitViewPlugin = sortingUnitViewPlugins(plugins).filter(p => (p.name === 'MVSortingUnitView'))[0];
    return (React.createElement(Fragment, null,
        React.createElement("div", { key: "sortingViews", style: { flexFlow: 'wrap' } }, sortByPriority(sortingViewPlugins(plugins)).filter(p => (p.name !== 'MVSortingView')).map(sv => (React.createElement(LaunchSortingViewButton, { key: sv.name, plugin: sv, onLaunch: onLaunchSortingView })))),
        React.createElement("div", { key: "view-single-unit" }, sortingUnitViewPlugin && (selection.selectedUnitIds || []).map(unitId => (React.createElement(LaunchSortingUnitViewButton, { key: 'unit-' + unitId, plugin: sortingUnitViewPlugin, unitId: unitId, label: `Unit ${unitId}`, onLaunch: onLaunchSortingUnitView }))))));
};
const LaunchSortingViewButton = ({ plugin, onLaunch }) => {
    const handleClick = useCallback(() => {
        onLaunch(plugin);
    }, [onLaunch, plugin]);
    return (React.createElement("button", { onClick: handleClick, style: buttonStyle },
        plugin.icon && (React.createElement(plugin.icon.type, Object.assign({}, plugin.icon.props, { style: { height: 14, width: 14, paddingRight: 2, paddingTop: 0 } }))),
        plugin.label));
};
const LaunchSortingUnitViewButton = ({ plugin, unitId, label, onLaunch }) => {
    const handleClick = useCallback(() => {
        onLaunch(plugin, unitId, label);
    }, [onLaunch, plugin, unitId, label]);
    return (React.createElement("button", { onClick: handleClick, style: buttonStyle },
        plugin.icon && React.createElement("span", { style: { paddingRight: 5 } }, plugin.icon),
        label));
};
export default ViewLauncher;
//# sourceMappingURL=ViewLauncher.js.map