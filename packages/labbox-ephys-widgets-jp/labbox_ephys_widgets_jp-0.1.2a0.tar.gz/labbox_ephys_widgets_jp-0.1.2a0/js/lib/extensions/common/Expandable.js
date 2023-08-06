import { Accordion, AccordionDetails, AccordionSummary } from '@material-ui/core';
import React from 'react';
export const Expandable = (props) => {
    return (React.createElement(Accordion, { TransitionProps: { unmountOnExit: props.unmountOnExit !== undefined ? props.unmountOnExit : true }, defaultExpanded: props.defaultExpanded },
        React.createElement(AccordionSummary, null,
            props.icon && React.createElement("span", { style: { paddingRight: 10 } }, props.icon),
            React.createElement("span", { style: { paddingTop: 3 } }, props.label)),
        React.createElement(AccordionDetails, null,
            React.createElement("div", { style: { width: "100%" } }, props.children))));
};
export default Expandable;
//# sourceMappingURL=Expandable.js.map