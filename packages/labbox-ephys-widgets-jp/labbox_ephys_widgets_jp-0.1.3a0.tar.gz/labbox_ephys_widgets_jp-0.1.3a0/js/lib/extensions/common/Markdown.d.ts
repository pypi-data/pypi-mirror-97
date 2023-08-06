import 'github-markdown-css';
import { FunctionComponent } from 'react';
interface Props {
    source: string;
    substitute?: {
        [key: string]: string | undefined | null;
    };
}
declare const Markdown: FunctionComponent<Props>;
export default Markdown;
