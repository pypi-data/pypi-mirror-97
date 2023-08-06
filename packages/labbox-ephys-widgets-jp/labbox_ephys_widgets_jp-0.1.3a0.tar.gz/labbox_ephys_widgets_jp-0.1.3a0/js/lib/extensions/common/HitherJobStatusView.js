import { Box, CircularProgress } from '@material-ui/core';
import React from 'react';
const HitherJobStatusView = ({ job, message = '', width = 200, height = 200 }) => {
    if (!job)
        return React.createElement("div", null, "No job");
    return (React.createElement(Box, { display: "flex", width: width, height: height },
        React.createElement(Box, { m: "auto" }, job.status === 'running' ? (React.createElement("span", null,
            "[",
            message,
            "] ",
            React.createElement(CircularProgress, null))) : job.status === 'error' ? (React.createElement("span", null,
            "Error: ",
            job.error_message,
            " [",
            message,
            "]")) : job.status === 'pending' ? (React.createElement("span", null, message)) : (React.createElement("span", null,
            "[",
            message,
            "] ",
            job.status)))));
};
export default HitherJobStatusView;
//# sourceMappingURL=HitherJobStatusView.js.map