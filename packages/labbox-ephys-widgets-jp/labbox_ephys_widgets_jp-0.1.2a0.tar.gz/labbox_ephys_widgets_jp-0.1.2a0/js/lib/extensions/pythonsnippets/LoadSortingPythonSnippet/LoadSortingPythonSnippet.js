import React from 'react';
import sizeMe from 'react-sizeme';
import Markdown from '../../common/Markdown';
import snippetMd from './load_sorting.md.gen';
const LoadSortingPythonSnippet = ({ size, sorting, recording }) => {
    const substitute = (md) => {
        let ret = md;
        ret = ret.replace('<SORTING_PATH>', sorting.sortingPath);
        return ret;
    };
    return (React.createElement(Markdown, { source: substitute(snippetMd) }));
};
export default sizeMe()(LoadSortingPythonSnippet);
//# sourceMappingURL=LoadSortingPythonSnippet.js.map