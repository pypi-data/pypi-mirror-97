import React from "react";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { coy } from "react-syntax-highlighter/dist/esm/styles/prism";
const MarkdownCodeBlock = ({ value, language = undefined }) => {
    return (React.createElement(SyntaxHighlighter, { language: language, style: coy }, value));
};
export default MarkdownCodeBlock;
//# sourceMappingURL=MarkdownCodeBlock.js.map