import { Toolbar } from '@material-ui/core';
import React, { useState } from 'react';
import Hyperlink from '../../common/Hyperlink';
const TimeWidgetBottomBar = (props) => {
    const { info, height, onCurrentTimeChanged } = props;
    // const style0 = {
    //     position: 'relative',
    //     width: this.props.width,
    //     height: this.props.height
    // };
    return (React.createElement(Toolbar, { style: { minHeight: height } },
        React.createElement(CurrentTimeControl, { width: 180, currentTime: info.currentTime || null, samplerate: info.samplerate, onChange: onCurrentTimeChanged }),
        "\u00A0",
        React.createElement(TimeRangeControl, { width: 250, timeRange: info.timeRange || null, samplerate: info.samplerate, onChange: props.onTimeRangeChanged }),
        React.createElement("span", null, info.statusText)));
};
const CurrentTimeControl = (props) => {
    const { currentTime, samplerate, width, onChange } = props;
    const _handleChange = (txt) => {
        let t = fromHumanTime(txt, samplerate);
        if (t !== undefined) {
            onChange(t);
        }
        else {
            console.warn(`Invalid human time string: ${txt}`);
        }
    };
    let style0 = {
        width,
        padding: 5,
        border: 'solid 1px lightgray'
    };
    return (React.createElement("div", { style: style0 },
        "Time:\u00A0",
        React.createElement(EditableText, { width: width - 50, title: "Click to edit current time", text: toHumanTime(currentTime, samplerate), onChange: _handleChange })));
};
const TimeRangeControl = (props) => {
    const _handleChange = (txt) => {
        let tr = fromHumanTimeRange(txt, props.samplerate);
        if ((tr === undefined) || (tr === null)) {
            console.warn(`Invalid human time range string: ${txt}`);
        }
        else {
            props.onChange(tr);
        }
    };
    const { timeRange, samplerate } = props;
    let style0 = {
        width: props.width,
        padding: 5,
        border: 'solid 1px lightgray'
    };
    return (React.createElement("div", { style: style0 },
        "Range:\u00A0",
        React.createElement(EditableText, { width: props.width - 50, title: "Click to edit time range", text: toHumanTimeRange(timeRange, samplerate), onChange: _handleChange })));
};
const toHumanTimeRange = (tr, samplerate) => {
    if (!tr)
        return 'none';
    return `${toHumanTime(tr.min, samplerate, { nounits: true, num_digits: 3 })} - ${toHumanTime(tr.max, samplerate, { num_digits: 3 })}`;
};
function fromHumanTimeRange(txt, samplerate) {
    if (txt === 'none')
        return null;
    let a = txt.split('-');
    if (a.length !== 2)
        return undefined;
    let t1 = fromHumanTime(a[0], samplerate, { nounits: true });
    let t2 = fromHumanTime(a[1], samplerate);
    if ((t1 === undefined) || (t2 === undefined))
        return undefined;
    return { min: t1, max: t2 };
}
const toHumanTime = (t, samplerate, opts = {}) => {
    if (t === null)
        return 'none';
    let sec = round(t / samplerate, opts.num_digits || 6);
    if (opts.nounits)
        return sec + '';
    else
        return `${sec} s`;
};
const fromHumanTime = (txt, samplerate, opts = {}) => {
    if (txt === 'none')
        return undefined;
    const list = txt.split(/(\s+)/).filter(e => e.trim().length > 0);
    if (list.length === 1) {
        if (opts.nounits) {
            return fromHumanTime(txt + ' s', samplerate, { nounits: false });
        }
        if (txt.endsWith('s'))
            return fromHumanTime(txt.slice(0, txt.length - 1) + ' s', samplerate);
        else
            return undefined;
    }
    else if (list.length === 2) {
        let val = Number(list[0]);
        if (isNaN(val))
            return undefined;
        let units = list[1];
        if (units === 's') {
            return val * samplerate;
        }
        else {
            return undefined;
        }
    }
    else {
        return undefined;
    }
};
const round = (val, num_digits) => {
    return Math.round(val * Math.pow(10, num_digits)) / Math.pow(10, num_digits);
};
const EditableText = (props) => {
    const [clicked, setClicked] = useState(false);
    const [editedText, setEditedText] = useState('');
    const _handleClick = () => {
        if (clicked)
            return;
        setClicked(true);
        setEditedText(props.text);
    };
    const _handleUnclick = () => {
        setClicked(false);
        props.onChange(editedText);
    };
    const _handleEditedTextChanged = (evt) => {
        setEditedText(evt.target.value);
    };
    const _handleKeyDown = (e) => {
        if (e.key === 'Enter') {
            _handleUnclick();
        }
    };
    let style0 = {
        width: props.width
    };
    let link0 = React.createElement("span", null);
    if (clicked) {
        link0 = (React.createElement("input", { type: "text", value: editedText, readOnly: false, onFocus: e => e.target.select(), onBlur: () => { _handleUnclick(); }, autoFocus: true, style: style0, onChange: (e) => { _handleEditedTextChanged(e); }, onKeyDown: (e) => { _handleKeyDown(e); } }));
    }
    else {
        let text = props.text;
        link0 = (React.createElement("span", { title: props.title },
            React.createElement(Hyperlink, { onClick: _handleClick },
                React.createElement("span", null, text))));
    }
    return link0;
};
export default TimeWidgetBottomBar;
//# sourceMappingURL=TimeWidgetBottomBar.js.map