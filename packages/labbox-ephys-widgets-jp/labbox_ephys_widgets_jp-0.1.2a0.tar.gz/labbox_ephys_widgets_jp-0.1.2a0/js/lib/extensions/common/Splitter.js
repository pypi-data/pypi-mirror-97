import React, { useState } from 'react';
import Draggable from 'react-draggable';
const defaultGripThickness = 10;
const defaultGripInnerThickness = 4;
const defaultGripMargin = 2;
const Splitter = (props) => {
    var _a, _b, _c;
    const { width, height, initialPosition, onChange, adjustable = true, positionFromRight = false } = props;
    const [gripPosition, setGripPosition] = useState(initialPosition);
    if (!props.children)
        throw Error('Unexpected: no props.children');
    let child1;
    let child2;
    if (!Array.isArray(props.children)) {
        child1 = props.children;
        child2 = null;
    }
    else {
        const children = props.children.filter(c => (c !== undefined));
        child1 = children[0];
        child2 = children[1] || null;
    }
    if (!child2) {
        return React.createElement(child1.type, Object.assign({}, child1.props, { width: width, height: height }));
    }
    const gripPositionFromLeft = positionFromRight ? width - gripPosition : gripPosition;
    const gripThickness = adjustable ? ((_a = props.gripThickness) !== null && _a !== void 0 ? _a : defaultGripThickness) : 0;
    const gripInnerThickness = adjustable ? ((_b = props.gripInnerThickness) !== null && _b !== void 0 ? _b : defaultGripInnerThickness) : 0;
    const gripMargin = adjustable ? ((_c = props.gripMargin) !== null && _c !== void 0 ? _c : defaultGripMargin) : 0;
    const width1 = gripPositionFromLeft - gripThickness / 2 - gripMargin;
    const width2 = width - width1 - gripThickness - 2 * gripMargin;
    let style0 = {
        top: 0,
        left: 0,
        width: width,
        height: height
    };
    let style1 = {
        left: 0,
        top: 0,
        width: width1,
        height: height,
        zIndex: 0,
        overflowY: 'auto',
        overflowX: 'hidden'
    };
    let style2 = {
        left: width1 + gripThickness + 2 * gripMargin,
        top: 0,
        width: width2,
        height: height,
        zIndex: 0,
        overflowY: 'auto',
        overflowX: 'hidden'
    };
    let styleGripOuter = {
        left: 0,
        top: 0,
        width: gripThickness + 2 * gripMargin,
        height: height,
        backgroundColor: 'transparent',
        cursor: 'col-resize',
        zIndex: 9998
    };
    let styleGrip = {
        left: gripMargin,
        top: 0,
        width: gripThickness,
        height: height,
        background: 'rgb(230, 230, 230)',
        cursor: 'col-resize'
    };
    let styleGripInner = {
        top: 0,
        left: (gripThickness - gripInnerThickness) / 2,
        width: gripInnerThickness,
        height: height,
        background: 'gray',
        cursor: 'col-resize'
    };
    const _handleGripDrag = (evt, ui) => {
    };
    const _handleGripDragStop = (evt, ui) => {
        const newGripPositionFromLeft = ui.x;
        if (newGripPositionFromLeft === gripPositionFromLeft) {
            return;
        }
        const newGripPosition = positionFromRight ? width - newGripPositionFromLeft : newGripPositionFromLeft;
        setGripPosition(newGripPosition);
        onChange && onChange(newGripPosition);
    };
    return (React.createElement("div", { className: "splitter", style: Object.assign(Object.assign({}, style0), { position: 'relative' }) },
        React.createElement("div", { key: "child1", style: Object.assign(Object.assign({}, style1), { position: 'absolute' }), className: "SplitterChild" },
            React.createElement(child1.type, Object.assign({}, child1.props, { width: width1, height: height }))),
        adjustable && (React.createElement(Draggable, { key: "drag", position: { x: gripPositionFromLeft - gripThickness / 2 - gripMargin, y: 0 }, axis: "x", onDrag: (evt, ui) => _handleGripDrag(evt, ui), onStop: (evt, ui) => _handleGripDragStop(evt, ui) },
            React.createElement("div", { style: Object.assign(Object.assign({}, styleGripOuter), { position: 'absolute' }) },
                React.createElement("div", { style: Object.assign(Object.assign({}, styleGrip), { position: 'absolute' }) },
                    React.createElement("div", { style: Object.assign(Object.assign({}, styleGripInner), { position: 'absolute' }) }))))),
        React.createElement("div", { key: "child2", style: Object.assign(Object.assign({}, style2), { position: 'absolute' }), className: "SplitterChild" },
            React.createElement(child2.type, Object.assign({}, child2.props, { width: width2, height: height })))));
};
export default Splitter;
//# sourceMappingURL=Splitter.js.map