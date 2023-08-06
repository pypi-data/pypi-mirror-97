import { FormControl, FormHelperText, makeStyles, MenuItem, Select } from '@material-ui/core';
import React from 'react';
const useStyles = makeStyles((theme) => ({
    formControl: {
        margin: theme.spacing(1),
        minWidth: 120,
    },
    selectEmpty: {
        marginTop: theme.spacing(2),
    },
}));
const DropdownControl = ({ label, value, onSetValue, options }) => {
    const classes = useStyles();
    return (React.createElement(FormControl, { className: classes.formControl },
        React.createElement(Select, { value: value, onChange: (evt) => onSetValue(evt.target.value), displayEmpty: true, className: classes.selectEmpty, inputProps: { 'aria-label': label } }, options.map(opt => (React.createElement(MenuItem, { value: opt.value, key: opt.label }, opt.label)))),
        React.createElement(FormHelperText, null, label)));
};
export default DropdownControl;
//# sourceMappingURL=DropdownControl.js.map