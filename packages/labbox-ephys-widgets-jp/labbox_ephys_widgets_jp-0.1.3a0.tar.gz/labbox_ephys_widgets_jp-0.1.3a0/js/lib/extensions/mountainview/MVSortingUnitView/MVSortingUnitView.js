import { Grid } from "@material-ui/core";
import { usePlugins } from "labbox";
import React, { Fragment } from 'react';
import Expandable from "../../common/Expandable";
import { sortingUnitViewPlugins } from "../../pluginInterface";
const MVSortingUnitView = (props) => {
    // important to exclude this plugin (not only for this widget but for all children) to avoid infinite recursion
    const plugins = usePlugins().filter(p => (p.name !== 'MVSortingUnitView'));
    const suvPlugins = sortingUnitViewPlugins(plugins);
    return (React.createElement(Fragment, null,
        React.createElement(Grid, { container: true, style: { flexFlow: 'wrap' }, spacing: 0 }, suvPlugins.filter(p => (!p.fullWidth)).map(suv => (React.createElement(Grid, { item: true, key: suv.name },
            React.createElement(suv.component, Object.assign({}, Object.assign(Object.assign({}, props), { plugins }), { width: 400, height: 400 })))))),
        React.createElement(Grid, { container: true, style: { flexFlow: 'column' }, spacing: 0 }, suvPlugins.filter(p => (p.fullWidth)).map(suv => (React.createElement(Grid, { item: true, key: suv.name },
            React.createElement(Expandable, { defaultExpanded: suv.defaultExpanded, label: suv.label },
                React.createElement(suv.component, Object.assign({}, Object.assign(Object.assign({}, props), { plugins }), { width: props.width, height: 400 })))))))));
};
export default MVSortingUnitView;
//# sourceMappingURL=MVSortingUnitView.js.map