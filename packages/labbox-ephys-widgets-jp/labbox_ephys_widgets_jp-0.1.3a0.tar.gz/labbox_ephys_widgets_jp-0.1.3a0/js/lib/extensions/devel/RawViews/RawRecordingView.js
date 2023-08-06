import React from 'react';
const RawRecordingView = ({ recording }) => {
    return (React.createElement("div", null,
        React.createElement("pre", null, JSON.stringify(recording, null, 4))));
};
export default RawRecordingView;
//# sourceMappingURL=RawRecordingView.js.map