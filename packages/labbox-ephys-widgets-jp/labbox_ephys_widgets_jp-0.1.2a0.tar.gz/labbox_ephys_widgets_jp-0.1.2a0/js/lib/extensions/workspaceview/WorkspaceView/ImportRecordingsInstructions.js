import React, { useCallback, useState } from 'react';
import Expandable from '../../common/Expandable';
import Markdown from '../../common/Markdown';
import import_example_simulated_recording_py from './importExamples/import_example_simulated_recording.py.gen';
import import_nwb_recording_py from './importExamples/import_nwb_recording.py.gen';
import import_spikeforest_recording_py from './importExamples/import_spikeforest_recording.py.gen';
import instructionsMd from './ImportRecordingsInstructions.md.gen';
const ImportRecordingsInstructions = ({ workspaceRoute }) => {
    const s = (x) => {
        return doSubstitute(x, {
            workspaceUri: workspaceRoute.workspaceUri
        });
    };
    return (React.createElement("div", null,
        React.createElement(Markdown, { source: instructionsMd }),
        React.createElement(Expandable, { label: "Import example simulated recording" },
            React.createElement(CopyToClipboardButton, { text: s(import_example_simulated_recording_py) }),
            React.createElement(Markdown, { source: mdWrapPy(s(import_example_simulated_recording_py)) })),
        React.createElement(Expandable, { label: "Import SpikeForest recordings" },
            React.createElement(CopyToClipboardButton, { text: s(import_spikeforest_recording_py) }),
            React.createElement(Markdown, { source: mdWrapPy(s(import_spikeforest_recording_py)) })),
        React.createElement(Expandable, { label: "Import NWB recordings" },
            React.createElement(CopyToClipboardButton, { text: s(import_nwb_recording_py) }),
            React.createElement(Markdown, { source: mdWrapPy(s(import_nwb_recording_py)) }))));
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
export default ImportRecordingsInstructions;
//# sourceMappingURL=ImportRecordingsInstructions.js.map