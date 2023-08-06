import { FunctionComponent } from 'react';
interface Props {
    label: string;
    defaultExpanded?: boolean;
    icon?: JSX.Element;
    unmountOnExit?: boolean;
}
export declare const Expandable: FunctionComponent<Props>;
export default Expandable;
