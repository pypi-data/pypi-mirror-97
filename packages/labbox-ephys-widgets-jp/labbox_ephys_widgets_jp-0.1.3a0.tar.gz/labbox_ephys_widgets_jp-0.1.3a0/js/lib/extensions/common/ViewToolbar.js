import { IconButton } from '@material-ui/core';
import React, { useMemo } from 'react';
const iconButtonStyle = { paddingLeft: 6, paddingRight: 6, paddingTop: 4, paddingBottom: 4 };
const ViewToolbar = (props) => {
    const toolbarStyle = useMemo(() => ({
        width: props.width,
        height: props.height,
        overflow: 'hidden'
    }), [props.width, props.height]);
    const buttons = useMemo(() => {
        const b = [];
        for (let a of (props.customActions || [])) {
            b.push({
                type: a.type || 'button',
                title: a.title,
                onClick: a.callback,
                icon: a.icon,
                selected: a.selected
            });
        }
        return b;
    }, [props.customActions]);
    return (React.createElement("div", { className: "ViewToolBar", style: Object.assign({ position: 'absolute' }, toolbarStyle) }, buttons.map((button, ii) => {
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
export default ViewToolbar;
//# sourceMappingURL=ViewToolbar.js.map