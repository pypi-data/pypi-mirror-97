import { ClickEventType } from '../../common/CanvasWidget/CanvasWidgetLayer';
export const paintAnimationLayer = (painter, props, state) => {
    painter.wipe(); // avoids afterimages. Placing before the short-circuit return also cleans up when done.
    if (!(state === null || state === void 0 ? void 0 : state.points) || state.points.length === 0)
        return;
    for (let pt of state.points) {
        const maxRadius = 20; // proof-of-concept; in practice this might be attached to the data record
        const currentRadius = Math.floor(maxRadius * pt.pct);
        const blueLevel = Math.floor(255 * pt.pct);
        const redLevel = Math.floor(255 - (255 * pt.pct));
        // const pen = { color: `rgb(${redLevel}, 0, ${blueLevel})`, width: 2}
        const brush = { color: `rgb(${redLevel}, 0, ${blueLevel})` };
        const boundingBox = {
            xmin: pt.loc[0] - currentRadius,
            ymin: pt.loc[1] - currentRadius,
            xmax: pt.loc[0] + currentRadius,
            ymax: pt.loc[1] + currentRadius
        };
        painter.fillEllipse(boundingBox, brush);
    }
};
// NOTE: Possible race condition in adding new points.
// If this were actually something important, we'd want to use a safer multiprocessing model for it.
const animate = (layer, timeStamp) => {
    var _a, _b, _c, _d, _e;
    const nextFrame = (stamp) => {
        return animate(layer, stamp);
    };
    const state = layer.getState();
    // update data for the points
    const candidatePts = (_a = state === null || state === void 0 ? void 0 : state.points) !== null && _a !== void 0 ? _a : [];
    while ((_c = (_b = state === null || state === void 0 ? void 0 : state.newQueue) === null || _b === void 0 ? void 0 : _b.length) !== null && _c !== void 0 ? _c : -1 > 0) {
        const pt = state === null || state === void 0 ? void 0 : state.newQueue.shift();
        pt && candidatePts.push(pt);
    }
    const pts = candidatePts.filter((pt) => !pt.done);
    for (let pt of pts) {
        pt.pct = (Math.min(pt.end, timeStamp) - pt.start) / (pt.end - pt.start);
        pt.done = pt.pct === 1;
    }
    const newState = layer.getState();
    layer.setState(Object.assign(Object.assign({}, newState), { points: pts }));
    layer.scheduleRepaint();
    if ((_e = (_d = newState === null || newState === void 0 ? void 0 : newState.points) === null || _d === void 0 ? void 0 : _d.length) !== null && _e !== void 0 ? _e : -1 > 0) {
        window.requestAnimationFrame(nextFrame);
    }
};
export const handleAnimatedClick = (e, layer) => {
    var _a;
    if (e.type !== ClickEventType.Press)
        return;
    const now = performance.now();
    const duration = 250; //quarter-second
    const newPoint = {
        loc: e.point,
        start: now,
        end: now + duration,
        pct: 0,
        done: false
    };
    const state = layer.getState();
    const pts = (_a = state === null || state === void 0 ? void 0 : state.newQueue) !== null && _a !== void 0 ? _a : [];
    pts.push(newPoint);
    layer.setState(Object.assign(Object.assign({}, layer.getState()), { newQueue: pts }));
    animate(layer, now);
};
//# sourceMappingURL=AnimatedLayer.js.map