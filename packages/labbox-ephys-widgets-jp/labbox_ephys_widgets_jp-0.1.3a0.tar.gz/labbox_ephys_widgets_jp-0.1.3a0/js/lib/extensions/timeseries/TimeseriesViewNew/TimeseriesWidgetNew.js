import React, { useCallback, useEffect, useMemo, useState } from 'react';
import { FaArrowDown, FaArrowUp } from 'react-icons/fa';
import { PainterPath } from '../../common/CanvasWidget';
import useBufferedDispatch from '../../common/useBufferedDispatch';
import { recordingSelectionReducer } from "../../pluginInterface";
import TimeWidgetNew from '../TimeWidgetNew/TimeWidgetNew';
const channelColors = [
    'rgb(80,80,80)',
    'rgb(104,42,42)',
    'rgb(42,104,42)',
    'rgb(42,42,152)'
];
class Panel {
    constructor(channelIndex, channelId, timeseriesData, y_offset, y_scale_factor) {
        this.channelIndex = channelIndex;
        this.channelId = channelId;
        this.timeseriesData = timeseriesData;
        this.y_offset = y_offset;
        this.y_scale_factor = y_scale_factor;
        // _updateHandler: (() => void) | null = null
        this._timeRange = null;
        this._yScale = 1;
        this._pixelWidth = null; // for determining the downsampling factor
        // timeseriesData.onDataSegmentSet((ds_factor, t1, t2) => {
        //     const timeRange = this._timeRange
        //     if (!timeRange) return
        //     if ((t1 <= timeRange.max) && (t2 >= timeRange.min)) {
        //         this._updateHandler && this._updateHandler()
        //     }
        // })
    }
    setTimeRange(timeRange) {
        this._timeRange = timeRange;
    }
    setYScale(s) {
        if (this._yScale === s)
            return;
        this._yScale = s;
        // this._updateHandler && this._updateHandler()
    }
    setPixelWidth(w) {
        if (this._pixelWidth === w)
            return;
        this._pixelWidth = w;
        // this._updateHandler && this._updateHandler()
    }
    paint(painter, completenessFactor) {
        const timeRange = this._timeRange;
        if (!timeRange)
            return;
        let downsample_factor = this._determineDownsampleFactor(completenessFactor);
        if (downsample_factor === null)
            return;
        let t1, t2, t1b, t2b;
        let data;
        while (true) {
            t1 = timeRange.min;
            t2 = timeRange.max;
            t1b = Math.floor(t1 / downsample_factor);
            t2b = Math.floor(t2 / downsample_factor);
            data = this.timeseriesData.getChannelData(this.channelIndex, t1b, t2b, downsample_factor); // todo: ds factor
            if (data.filter(x => (isNaN(x))).length === 0) {
                break;
            }
            if ((t2b - t1b < 200) || (downsample_factor > 100)) {
                break;
            }
            downsample_factor *= 3;
        }
        const pp = new PainterPath();
        if (downsample_factor === 1) {
            let penDown = false;
            for (let tt = t1; tt < t2; tt++) {
                let val = data[tt - t1];
                if (!isNaN(val)) {
                    let val2 = ((val + this.y_offset) * this.y_scale_factor * this._yScale) / 2 + 0.5;
                    if (penDown) {
                        pp.lineTo(tt, val2);
                    }
                    else {
                        pp.moveTo(tt, val2);
                        penDown = true;
                    }
                }
                else {
                    penDown = false;
                }
            }
        }
        else {
            let penDown = false;
            for (let tt = t1b; tt < t2b; tt++) {
                let val_min = data[(tt - t1b) * 2];
                let val_max = data[(tt - t1b) * 2 + 1];
                if ((!isNaN(val_min)) && (!isNaN(val_max))) {
                    let val2_min = ((val_min + this.y_offset) * this.y_scale_factor * this._yScale) / 2 + 0.5;
                    let val2_max = ((val_max + this.y_offset) * this.y_scale_factor * this._yScale) / 2 + 0.5;
                    if (penDown) {
                        pp.lineTo((tt - 1 / 3) * downsample_factor, val2_min);
                        pp.lineTo((tt + 1 / 3) * downsample_factor, val2_max);
                    }
                    else {
                        pp.moveTo((tt - 1 / 3) * downsample_factor, val2_min);
                        pp.lineTo((tt + 1 / 3) * downsample_factor, val2_max);
                        penDown = true;
                    }
                }
                else {
                    penDown = false;
                }
            }
        }
        const color = channelColors[this.channelIndex % channelColors.length];
        const pen = { color, width: 1 };
        painter.drawPath(pp, pen);
    }
    _determineDownsampleFactor(completenessFactor) {
        let timeRange = this._timeRange;
        if (!timeRange)
            return null;
        if (this._pixelWidth === null)
            return null;
        const numChannels = this.timeseriesData.numChannels();
        let factor0 = 1.3; // this is a tradeoff between rendering speed and appearance
        if (numChannels > 32) {
            factor0 = 0.5;
        }
        // determine what the downsample factor should be based on the number
        // of timepoints in the view range
        // we also need to consider the number of pixels it corresponds to
        const targetNumPix = Math.max(500, this._pixelWidth * factor0) * completenessFactor;
        const numPoints = timeRange.max - timeRange.min;
        let ds_factor = 1;
        let factor = 3;
        while (numPoints / (ds_factor * factor) > targetNumPix) {
            ds_factor *= factor;
        }
        return ds_factor;
    }
    label() {
        return this.channelId + '';
    }
}
const TimeseriesWidgetNew = (props) => {
    const { timeseriesData, width, height, y_scale_factor, channel_ids, visibleChannelIds, recordingSelection: externalSelection, recordingSelectionDispatch: externalSelectionDispatch } = props;
    const [panels, setPanels] = useState([]);
    const [recordingSelection, recordingSelectionDispatch] = useBufferedDispatch(recordingSelectionReducer, externalSelection, useMemo(() => ((state) => { externalSelectionDispatch({ type: 'Set', state }); }), [externalSelectionDispatch]), 400);
    const [actions, setActions] = useState(null);
    const _handleScaleAmplitudeUp = useCallback(() => {
        recordingSelectionDispatch({ type: 'ScaleAmpScaleFactor', direction: 'up' });
    }, [recordingSelectionDispatch]);
    const _handleScaleAmplitudeDown = useCallback(() => {
        recordingSelectionDispatch({ type: 'ScaleAmpScaleFactor', direction: 'down' });
    }, [recordingSelectionDispatch]);
    useEffect(() => {
        const panels0 = [];
        for (let ch = 0; ch < timeseriesData.numChannels(); ch++) {
            // todo: i guess we need to redefine the panels whenever y_offsets or y_scale_factor or channel_ids change
            const channel_id = channel_ids[ch];
            if ((!visibleChannelIds) || (visibleChannelIds.includes(channel_id))) {
                const p = new Panel(ch, channel_id, timeseriesData, 0, y_scale_factor); // y_offsets[ch] replaced with 0
                p.setPixelWidth(width);
                p.setYScale(recordingSelection.ampScaleFactor || 1);
                panels0.push(p);
            }
        }
        setPanels(panels0);
    }, [channel_ids, setPanels, timeseriesData, y_scale_factor, visibleChannelIds, width, recordingSelection.ampScaleFactor, recordingSelection.timeRange]);
    useEffect(() => {
        if (actions === null) {
            const a = [
                {
                    type: 'button',
                    callback: _handleScaleAmplitudeUp,
                    title: 'Scale amplitude up [up arrow]',
                    icon: React.createElement(FaArrowUp, null),
                    keyCode: 38
                },
                {
                    type: 'button',
                    callback: _handleScaleAmplitudeDown,
                    title: 'Scale amplitude down [down arrow]',
                    icon: React.createElement(FaArrowDown, null),
                    keyCode: 40
                },
                {
                    type: 'divider'
                }
            ];
            setActions(a);
        }
    }, [actions, setActions, _handleScaleAmplitudeDown, _handleScaleAmplitudeUp, recordingSelection.ampScaleFactor, width]);
    const numTimepoints = useMemo(() => (timeseriesData ? timeseriesData.numTimepoints() : 0), [timeseriesData]);
    return (React.createElement(TimeWidgetNew, { panels: panels, customActions: actions, width: width, height: height, samplerate: timeseriesData.getSampleRate(), startTimeSpan: 1e7 / timeseriesData.numChannels(), maxTimeSpan: 1e7 / timeseriesData.numChannels(), numTimepoints: numTimepoints, selection: recordingSelection, selectionDispatch: recordingSelectionDispatch }));
};
export default TimeseriesWidgetNew;
//# sourceMappingURL=TimeseriesWidgetNew.js.map