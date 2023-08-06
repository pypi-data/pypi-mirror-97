import { IconButton, Tab, Tabs } from '@material-ui/core';
import CheckBoxOutlineBlankIcon from '@material-ui/icons/CheckBoxOutlineBlank';
import CloseIcon from "@material-ui/icons/Close";
import { default as React, useCallback, useEffect, useMemo } from 'react';
const ViewContainerTabBar = ({ views, currentView, onCurrentViewChanged, onViewClosed, active }) => {
    useEffect(() => {
        const i = currentView ? views.indexOf(currentView) : -1;
        if (i < 0) {
            if (views.length > 0) {
                onCurrentViewChanged(views[0]);
            }
        }
    }, [currentView, onCurrentViewChanged, views]);
    const handleClickView = useCallback((v) => {
        onCurrentViewChanged(v);
    }, [onCurrentViewChanged]);
    let currentIndex = currentView ? views.indexOf(currentView) : null;
    if (currentIndex === -1)
        currentIndex = null;
    const classes = ['ViewContainerTabBar'];
    if (active)
        classes.push('active');
    const opts = useMemo(() => (views.map((v, i) => ({ selected: (i === (currentIndex || 0)) }))), [views, currentIndex]);
    return (React.createElement(Tabs, { value: currentIndex || 0, 
        // onChange={handleChange}
        scrollButtons: "auto", variant: "scrollable", className: classes.join(' ') }, views.map((v, i) => (React.createElement(ViewContainerTab, { key: i, view: v, onClick: handleClickView, onClose: onViewClosed, opts: opts[i] })))));
};
const ViewContainerTab = ({ view, onClose, opts, onClick }) => {
    // thanks: https://stackoverflow.com/questions/63265780/react-material-ui-tabs-close/63277341#63277341
    // thanks also: https://www.freecodecamp.org/news/reactjs-implement-drag-and-drop-feature-without-using-external-libraries-ad8994429f1a/
    const icon = useMemo(() => (view.plugin.icon || React.createElement(CheckBoxOutlineBlankIcon, null)), [view.plugin.icon]);
    const handleClick = useCallback(() => {
        onClick(view);
    }, [onClick, view]);
    const label = (React.createElement("div", { style: { whiteSpace: 'nowrap' }, draggable: true, onDragStart: (e) => { e.dataTransfer.setData('viewId', view.viewId); }, onClick: handleClick },
        React.createElement(icon.type, Object.assign({}, icon.props, { style: { paddingRight: 5, paddingLeft: 3, paddingTop: 0, width: 20, height: 20, display: 'inline', verticalAlign: 'middle' } })),
        React.createElement("span", { style: { display: 'inline', verticalAlign: 'middle' } }, view.label),
        React.createElement("span", null, "\u00A0"),
        React.createElement(IconButton, { component: "div", onClick: () => onClose(view), className: "CloseButton", style: { padding: 0 } },
            React.createElement(CloseIcon, { style: {
                    display: 'inline',
                    verticalAlign: 'middle',
                    fontSize: 20
                } }))));
    const style = useMemo(() => (opts.selected ? { color: 'white', fontWeight: 'bold' } : { color: 'lightgray' }), [opts.selected]);
    return (React.createElement(Tab, { key: view.viewId, label: label, className: "Tab", style: style }));
};
export default ViewContainerTabBar;
//# sourceMappingURL=ViewContainerTabBar.js.map