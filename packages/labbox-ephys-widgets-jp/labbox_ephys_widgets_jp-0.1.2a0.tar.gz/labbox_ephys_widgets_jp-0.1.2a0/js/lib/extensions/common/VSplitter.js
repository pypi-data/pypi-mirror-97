import React, { useState } from 'react';
import Draggable from 'react-draggable';
const VSplitter = (props) => {
    var _a, _b, _c;
    const { width, height, initialPosition, onChange } = props;
    const [gripPosition, setGripPosition] = useState(initialPosition);
    if (!props.children)
        throw Error('Unexpected: no props.children');
    if (!Array.isArray(props.children)) {
        let child0 = props.children;
        return React.createElement(child0.type, Object.assign({}, child0.props, { width: width, height: height }));
    }
    const children = props.children.filter(c => (c !== undefined));
    let child1 = children[0];
    let child2 = children[1];
    if (child2 === undefined) {
        return React.createElement(child1.type, Object.assign({}, child1.props, { width: width, height: height }));
    }
    const gripThickness = (_a = props.gripThickness) !== null && _a !== void 0 ? _a : 12;
    const gripInnerThickness = (_b = props.gripInnerThickness) !== null && _b !== void 0 ? _b : 4;
    const gripMargin = (_c = props.gripMargin) !== null && _c !== void 0 ? _c : 4;
    const height1 = gripPosition - gripThickness / 2 - gripMargin;
    const height2 = height - height1 - gripThickness - 2 * gripMargin;
    let style0 = {
        top: 0,
        left: 0,
        width: width,
        height: height
    };
    let style1 = {
        left: 0,
        top: 0,
        width: width,
        height: height1,
        zIndex: 0,
        overflowY: 'auto',
        overflowX: 'hidden'
    };
    let style2 = {
        left: 0,
        top: height1 + gripThickness + 2 * gripMargin,
        width: width,
        height: height2,
        zIndex: 0,
        overflowY: 'auto',
        overflowX: 'hidden'
    };
    let styleGripOuter = {
        left: 0,
        top: 0,
        width: width,
        height: gripThickness + 2 * gripMargin,
        backgroundColor: 'transparent',
        cursor: 'row-resize',
        zIndex: 9998
    };
    let styleGrip = {
        left: 0,
        top: gripMargin,
        width: width,
        height: gripThickness,
        background: 'rgb(230, 230, 230)',
        cursor: 'row-resize'
    };
    let styleGripInner = {
        top: (gripThickness - gripInnerThickness) / 2,
        left: 0,
        width: width,
        height: gripInnerThickness,
        background: 'gray',
        cursor: 'row-resize'
    };
    const _handleGripDrag = (evt, ui) => {
    };
    const _handleGripDragStop = (evt, ui) => {
        const newGripPosition = ui.y;
        if (newGripPosition === gripPosition) {
            return;
        }
        setGripPosition(newGripPosition);
        onChange && onChange(newGripPosition);
    };
    return (React.createElement("div", { className: "vsplitter", style: Object.assign(Object.assign({}, style0), { position: 'relative' }) },
        React.createElement("div", { key: "child1", style: Object.assign(Object.assign({}, style1), { position: 'absolute' }), className: "VSplitterChild" },
            React.createElement(child1.type, Object.assign({}, child1.props, { width: width, height: height1 }))),
        React.createElement(Draggable, { key: "drag", position: { x: 0, y: gripPosition - gripThickness / 2 - gripMargin }, axis: "y", onDrag: (evt, ui) => _handleGripDrag(evt, ui), onStop: (evt, ui) => _handleGripDragStop(evt, ui) },
            React.createElement("div", { style: Object.assign(Object.assign({}, styleGripOuter), { position: 'absolute' }) },
                React.createElement("div", { style: Object.assign(Object.assign({}, styleGrip), { position: 'absolute' }) },
                    React.createElement("div", { style: Object.assign(Object.assign({}, styleGripInner), { position: 'absolute' }) })))),
        React.createElement("div", { key: "child2", style: Object.assign(Object.assign({}, style2), { position: 'absolute' }), className: "VSplitterChild" },
            React.createElement(child2.type, Object.assign({}, child2.props, { width: width, height: height2 })))));
};
export default VSplitter;
//# sourceMappingURL=VSplitter.js.map