/* eslint-disable no-use-before-define */
import { makeStyles } from '@material-ui/core/styles';
//import Autocomplete from '@material-ui/lab/Autocomplete';
import React from 'react';
// TODO: Import own css styling?
// May need to scrap the makestyles call
const useStyles = makeStyles((theme) => ({
    root: {
        width: 500,
        '& > * + *': {
            marginTop: theme.spacing(3),
        },
    },
}));
const MultiComboBox = ({ id, label, placeholder, onSelectionsChanged, getLabelFromOption = (x) => x, selectedOptionLabels = [], options = [] }) => {
    const classes = useStyles();
    return (React.createElement("div", { className: classes.root }));
};
export default MultiComboBox;
//# sourceMappingURL=MultiComboBox.js.map