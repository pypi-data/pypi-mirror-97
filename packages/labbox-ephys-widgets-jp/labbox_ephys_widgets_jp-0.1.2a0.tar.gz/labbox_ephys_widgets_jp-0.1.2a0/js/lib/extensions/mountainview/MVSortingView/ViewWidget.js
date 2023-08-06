import React from 'react';
const ViewWidget = ({ view, sortingViewProps, width, height }) => {
    const p = view.plugin;
    const Component = p.component;
    let pr = {};
    if (width)
        pr.width = width;
    if (height)
        pr.height = height;
    return (React.createElement(Component, Object.assign({}, sortingViewProps, pr, view.extraProps)));
};
export default ViewWidget;
//# sourceMappingURL=ViewWidget.js.map