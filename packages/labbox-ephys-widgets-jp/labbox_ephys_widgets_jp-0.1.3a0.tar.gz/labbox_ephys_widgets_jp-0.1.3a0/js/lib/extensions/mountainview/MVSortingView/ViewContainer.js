import React, { useCallback, useEffect, useState } from 'react';
import Draggable from 'react-draggable';
import ViewContainerTabBar from './ViewContainerTabBar';
// needs to correspond to css (not best system) - see mountainview.css
const tabBarHeight = 30 + 5;
const ViewContainer = ({ children, views, onViewClosed, onSetViewArea, width, height }) => {
    const [currentNorthView, setCurrentNorthView] = useState(null);
    const [currentSouthView, setCurrentSouthView] = useState(null);
    const [activeArea, setActiveArea] = useState('north');
    const [splitterFrac, setSplitterFrac] = useState(0.5);
    useEffect(() => {
        views.forEach(v => {
            if (!v.area)
                v.area = activeArea;
            if (v.activate) {
                v.activate = false;
                if (v.area === 'north') {
                    setCurrentNorthView(v);
                    setActiveArea('north');
                }
                else if (v.area === 'south') {
                    setCurrentSouthView(v);
                    setActiveArea('south');
                }
            }
        });
    }, [views, activeArea]);
    const hMargin = 3;
    const vMargin = 3;
    const W = (width || 300) - hMargin * 2;
    const H = height - vMargin * 2;
    const splitterHeight = 16;
    const a = (H - tabBarHeight * 2 - splitterHeight);
    const H1 = a * splitterFrac;
    const H2 = a * (1 - splitterFrac);
    const handleSplitterDelta = useCallback((delta) => {
        setSplitterFrac((H1 + delta) / (H1 + H2));
    }, [setSplitterFrac, H1, H2]);
    const areas = {
        'north': {
            tabBarStyle: { left: 0, top: 0, width: W, height: tabBarHeight },
            divStyle: { left: 0, top: tabBarHeight, width: W, height: H1 }
        },
        'south': {
            tabBarStyle: { left: 0, top: tabBarHeight + H1 + splitterHeight, width: W, height: tabBarHeight },
            divStyle: { left: 0, top: tabBarHeight * 2 + H1 + splitterHeight, width: W, height: H2 }
        }
    };
    const splitterStyle = {
        left: 0, top: tabBarHeight + H1, width: W, height: splitterHeight
    };
    const handleClick = useCallback((e) => {
        const y = eventToPos(e)[1];
        const newActiveArea = (y < tabBarHeight + H1) ? 'north' : 'south';
        if (newActiveArea !== activeArea) {
            setActiveArea(newActiveArea);
        }
    }, [H1, activeArea, setActiveArea]);
    const handleDragOver = useCallback((event) => {
        // the following is needed otherwise we can't get the drop. See: https://stackoverflow.com/questions/50230048/react-ondrop-is-not-firing
        event.stopPropagation();
        event.preventDefault();
    }, []);
    const handleDragDrop = useCallback((e) => {
        const y = eventToPos(e)[1];
        const dropArea = (y < tabBarHeight + H1) ? 'north' : 'south';
        const viewId = e.dataTransfer.getData('viewId');
        if (viewId) {
            const view = views.filter(v => v.viewId === viewId)[0];
            if (view) {
                if (view.area !== dropArea) {
                    onSetViewArea(view, dropArea);
                }
            }
        }
    }, [views, H1, onSetViewArea]);
    if (!Array.isArray(children)) {
        throw Error('Unexpected children in ViewContainer');
    }
    const children2 = children;
    return (React.createElement("div", { style: { position: 'absolute', left: hMargin, top: vMargin, width: W, height: H }, onClick: handleClick, onDragOver: handleDragOver, onDrop: handleDragDrop, className: "ViewContainer" },
        React.createElement("div", { key: "north-tab-bar", style: Object.assign({ position: 'absolute' }, areas['north'].tabBarStyle) },
            React.createElement(ViewContainerTabBar, { views: views.filter(v => v.area === 'north'), currentView: currentNorthView, onCurrentViewChanged: setCurrentNorthView, onViewClosed: onViewClosed, active: activeArea === 'north' })),
        React.createElement("div", { key: "south-tab-bar", style: Object.assign({ position: 'absolute' }, areas['south'].tabBarStyle) },
            React.createElement(ViewContainerTabBar, { views: views.filter(v => v.area === 'south'), currentView: currentSouthView, onCurrentViewChanged: setCurrentSouthView, onViewClosed: onViewClosed, active: activeArea === 'south' })),
        React.createElement("div", { key: "splitter", style: Object.assign(Object.assign({ position: 'absolute' }, splitterStyle), { zIndex: 9998 }) },
            React.createElement(SplitterGrip, { onDelta: handleSplitterDelta, width: W, height: splitterHeight })),
        children2.map(c => {
            const childView = c.props.view;
            const visible = ((childView.area === 'north') && (childView === currentNorthView)) || ((childView.area === 'south') && (childView === currentSouthView));
            const area = areas[childView.area || 'north'];
            return (React.createElement("div", { key: childView.viewId, style: Object.assign({ visibility: visible ? 'visible' : 'hidden', overflowY: 'auto', overflowX: 'hidden', position: 'absolute' }, area.divStyle) },
                React.createElement(c.type, Object.assign({}, c.props, { width: W, height: area.divStyle.height }))));
        })));
};
const SplitterGrip = ({ onDelta, width, height }) => {
    const handleGripDrag = useCallback((evt, ui) => {
    }, []);
    const handleGripDragStop = useCallback((evt, ui) => {
        const newGripPosition = ui.y;
        onDelta(newGripPosition);
    }, [onDelta]);
    const innerGripThickness = 4;
    return (React.createElement(Draggable, { key: "drag", position: { x: 0, y: 0 }, axis: "y", onDrag: handleGripDrag, onStop: handleGripDragStop },
        React.createElement("div", { style: {
                position: 'absolute',
                width,
                height,
                backgroundColor: 'white',
                cursor: 'row-resize'
            } },
            React.createElement("div", { style: {
                    position: 'absolute',
                    width,
                    top: (height - innerGripThickness) / 2,
                    height: innerGripThickness,
                    backgroundColor: 'gray'
                } }))));
};
const eventToPos = (e) => {
    const element = e.currentTarget;
    const x = e.clientX - element.getBoundingClientRect().x;
    const y = e.clientY - element.getBoundingClientRect().y;
    return [x, y];
};
export default ViewContainer;
//# sourceMappingURL=ViewContainer.js.map