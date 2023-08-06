import { IconButton } from '@material-ui/core';
import React from 'react';
import { FaArrowLeft, FaArrowRight, FaSearchMinus, FaSearchPlus } from 'react-icons/fa';
const iconButtonStyle = { paddingLeft: 6, paddingRight: 6, paddingTop: 4, paddingBottom: 4 };
const TimeWidgetToolbarNew = (props) => {
    const style0 = {
        width: props.width,
        height: props.height,
        top: props.top,
        overflow: 'hidden'
    };
    let buttons = [];
    buttons.push({
        type: 'button',
        title: "Time zoom in (+)",
        onClick: props.onZoomIn,
        icon: React.createElement(FaSearchPlus, null)
    });
    buttons.push({
        type: 'button',
        title: "Time zoom out (-)",
        onClick: props.onZoomOut,
        icon: React.createElement(FaSearchMinus, null)
    });
    buttons.push({
        type: 'button',
        title: "Shift time left [left arrow]",
        onClick: props.onShiftTimeLeft,
        icon: React.createElement(FaArrowLeft, null)
    });
    buttons.push({
        type: 'button',
        title: "Shift time right [right arrow]",
        onClick: props.onShiftTimeRight,
        icon: React.createElement(FaArrowRight, null)
    });
    buttons.push({
        type: 'divider'
    });
    for (let a of (props.customActions || [])) {
        buttons.push({
            type: a.type || 'button',
            title: a.title,
            onClick: a.callback,
            icon: a.icon,
            selected: a.selected
        });
    }
    return (React.createElement("div", { className: "TimeWidgetToolBar", style: Object.assign({ position: 'absolute' }, style0) }, buttons.map((button, ii) => {
        if (button.type === 'button') {
            let color = 'inherit';
            if (button.selected)
                color = 'primary';
            return (React.createElement(IconButton, { title: button.title, onClick: button.onClick, key: ii, color: color, style: iconButtonStyle }, button.icon));
        }
        else if (button.type === 'divider') {
            return React.createElement("hr", { key: ii });
        }
        else {
            return React.createElement("span", { key: ii });
        }
    })));
};
export default TimeWidgetToolbarNew;
//# sourceMappingURL=TimeWidgetToolbarNew.js.map