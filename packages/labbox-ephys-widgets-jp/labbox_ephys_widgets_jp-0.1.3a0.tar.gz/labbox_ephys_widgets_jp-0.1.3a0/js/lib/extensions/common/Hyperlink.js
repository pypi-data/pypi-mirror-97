import React from 'react';
const Hyperlink = (props) => {
    let style0 = {
        color: 'gray',
        cursor: 'pointer',
        textDecoration: 'underline'
    };
    return (React.createElement("span", { style: style0, onClick: props.onClick }, props.children));
};
export default Hyperlink;
//# sourceMappingURL=Hyperlink.js.map