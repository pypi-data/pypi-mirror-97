import 'github-markdown-css';
import React from 'react';
import ReactMarkdown from "react-markdown";
import MarkdownCodeBlock from "./MarkdownCodeBlock";
const Markdown = ({ source, substitute }) => {
    const source2 = substitute ? doSubstitute(source, substitute) : source;
    return (React.createElement("div", { className: 'markdown-body' },
        React.createElement(ReactMarkdown, { source: source2, renderers: { code: MarkdownCodeBlock } })));
};
const doSubstitute = (x, s) => {
    let y = x;
    for (let k in s) {
        y = y.split(`{${k}}`).join(s[k] || '');
    }
    return y;
};
export default Markdown;
//# sourceMappingURL=Markdown.js.map