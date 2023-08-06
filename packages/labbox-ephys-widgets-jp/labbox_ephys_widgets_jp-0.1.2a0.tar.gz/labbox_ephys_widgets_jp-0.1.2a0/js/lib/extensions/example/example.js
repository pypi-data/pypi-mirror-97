// LABBOX-EXTENSION: example
// LABBOX-EXTENSION-TAGS: jupyter
import React from 'react';
// Use recordingview snippet to insert a recording view
const ExampleRecordingView = ({ recording }) => {
    return (React.createElement("div", null,
        "Example recording view. Recording ID: ",
        recording.recordingId));
};
export function activate(context) {
    // Use registerrecordingview snippet to register a recording view
    context.registerPlugin({
        type: 'RecordingView',
        name: 'ExampleRecordingView',
        label: 'Example recording view',
        priority: 50,
        development: true,
        disabled: true,
        component: ExampleRecordingView
    });
}
//# sourceMappingURL=example.js.map