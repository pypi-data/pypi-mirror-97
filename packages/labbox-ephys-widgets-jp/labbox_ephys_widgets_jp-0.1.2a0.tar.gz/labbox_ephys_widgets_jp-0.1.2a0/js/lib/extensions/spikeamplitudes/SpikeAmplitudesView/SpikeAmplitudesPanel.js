import { getArrayMax, getArrayMin } from '../../common/Utility';
// const calculationPool = createCalculationPool({maxSimultaneous: 6})
const colorList = [
    'blue',
    'green',
    'red',
    'orange',
    'purple',
    'cyan'
];
const colorForUnitId = (unitId) => {
    if (Array.isArray(unitId))
        return colorForUnitId(Math.min(...unitId));
    while (unitId < 0)
        unitId += colorList.length;
    return colorList[unitId % colorList.length];
};
class SpikeAmplitudesPanel {
    constructor(args) {
        this.args = args;
        this._updateHandler = null;
        this._timeRange = null;
        this._calculationScheduled = false;
        this._calculationError = null;
        this._yrange = null;
        this._globalAmplitudeRange = null;
        this._includeZero = true;
        this._amplitudes = undefined;
    }
    setTimeRange(timeRange) {
        this._timeRange = timeRange;
    }
    paint(painter, completenessFactor) {
        const timeRange = this._timeRange;
        if (!timeRange)
            return;
        const font = { pixelSize: 12, family: 'Arial' };
        const color = colorForUnitId(this.args.unitId);
        const pen = { color: 'black' };
        const brush = { color };
        if (!this.args.spikeAmplitudesData)
            return;
        const result = this.args.spikeAmplitudesData.getSpikeAmplitudes(this.args.unitId);
        if ((result) && (result.timepoints) && (result.amplitudes)) {
            const { timepoints, amplitudes } = result;
            this._amplitudes = amplitudes;
            let yrange = this._yrange || this.autoYRange();
            if (!yrange)
                return;
            if (this._includeZero) {
                yrange = { min: Math.min(0, yrange.min), max: Math.max(0, yrange.max) };
            }
            painter.drawLine(timeRange.min, 0, timeRange.max, 0, { color: 'gray' });
            const N = timepoints.length;
            for (let i = 0; i < N; i++) {
                const t = timepoints[i];
                const a = amplitudes[i];
                const y = (a - yrange.min) / (yrange.max - yrange.min);
                if ((timeRange.min <= t) && (t <= timeRange.max)) {
                    painter.drawMarker([t, y], { radius: 3, pen, brush });
                }
            }
        }
        else {
            painter.drawText({
                rect: { xmin: timeRange.min, xmax: timeRange.max, ymin: 0, ymax: 1 },
                alignment: { Horizontal: 'AlignCenter', Vertical: 'AlignCenter' },
                font, pen, brush,
                text: 'calculating'
            });
        }
    }
    paintYAxis(painter, width, height) {
        paintYAxis(painter, { xmin: 0, xmax: width, ymin: 0, ymax: height }, { label: 'Spike amplitude' });
    }
    label() {
        return this.args.unitId + '';
    }
    amplitudeRange() {
        if (this._amplitudes) {
            return { min: getArrayMin(this._amplitudes), max: getArrayMax(this._amplitudes) };
        }
        else
            return null;
    }
    setGlobalAmplitudeRange(r) {
        this._globalAmplitudeRange = r;
    }
    autoYRange() {
        if (this._globalAmplitudeRange) {
            return this._globalAmplitudeRange;
        }
        return this.amplitudeRange();
    }
    setYRange(yrange) {
        this._yrange = yrange;
    }
    register(onUpdate) {
        this._updateHandler = onUpdate;
    }
}
const paintYAxis = (painter, pixelRect, { label }) => {
    const { xmin, xmax, ymin, ymax } = pixelRect;
    painter.drawLine(xmax, ymin, xmax, ymax, { color: 'black' });
    const tickSize = 10;
    painter.drawText({
        rect: { xmin, xmax: xmax - tickSize - 2, ymin, ymax },
        alignment: { Horizontal: 'AlignRight', Vertical: 'AlignCenter' },
        font: { family: 'Arial', pixelSize: 12 },
        pen: { color: 'black' },
        brush: { color: 'black' },
        text: label,
        orientation: 'Vertical'
    });
};
class CombinedPanel {
    constructor(panels, labelString) {
        this.panels = panels;
        this.labelString = labelString;
    }
    setTimeRange(timeRange) {
        this.panels.forEach(p => p.setTimeRange(timeRange));
    }
    paint(painter, completenessFactor) {
        this.panels.forEach(p => p.paint(painter, completenessFactor));
    }
    paintYAxis(painter, width, height) {
        const p = this.panels[0];
        p && p.paintYAxis && p.paintYAxis(painter, width, height);
    }
    label() {
        return this.labelString;
    }
    register(onUpdate) {
        this.panels.forEach(p => p.register(() => {
            onUpdate();
        }));
    }
}
export const combinePanels = (panels, label) => {
    return new CombinedPanel(panels, label);
};
export default SpikeAmplitudesPanel;
//# sourceMappingURL=SpikeAmplitudesPanel.js.map