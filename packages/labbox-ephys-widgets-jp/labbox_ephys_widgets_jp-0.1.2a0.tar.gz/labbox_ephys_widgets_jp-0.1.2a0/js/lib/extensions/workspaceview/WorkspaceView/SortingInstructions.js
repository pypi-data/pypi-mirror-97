import React, { useCallback, useState } from 'react';
import Expandable from '../../common/Expandable';
import Markdown from '../../common/Markdown';
import spykingcircus_example_py from './sortingExamples/spykingcircus_example.py.gen';
import instructionsMd from './SortingInstructions.md.gen';
const SortingInstructions = ({ workspaceRoute, recordingId, recordingLabel }) => {
    const s = (x) => {
        return doSubstitute(x, {
            workspaceUri: workspaceRoute.workspaceUri,
            recordingId,
            recordingLabel
        });
    };
    return (React.createElement("div", null,
        React.createElement(Markdown, { source: instructionsMd }),
        React.createElement(Expandable, { label: "SpyKING CIRCUS" },
            React.createElement(CopyToClipboardButton, { text: s(spykingcircus_example_py) }),
            React.createElement(Markdown, { source: mdWrapPy(s(spykingcircus_example_py)) }))));
};
const mdWrapPy = (py) => {
    return "```python\n" + py + '\n```';
};
const CopyToClipboardButton = ({ text }) => {
    const [copied, setCopied] = useState(false);
    const handleClick = useCallback(() => {
        // see: https://stackoverflow.com/questions/51805395/navigator-clipboard-is-undefined
        if (!window.isSecureContext) {
            window.alert('Unable to copy to clipbard (not a secure context). This is probably because this site uses http rather than https.');
            return;
        }
        navigator.clipboard.writeText(text);
        setCopied(true);
        setTimeout(() => {
            setCopied(false);
        }, 3000);
    }, [text]);
    return (React.createElement("button", { onClick: handleClick }, copied ? `Copied` : `Copy to clipboard`));
};
const doSubstitute = (x, s) => {
    let y = x;
    for (let k in s) {
        y = y.split(`{${k}}`).join(s[k] || '');
    }
    return y;
};
export default SortingInstructions;
//# sourceMappingURL=SortingInstructions.js.map