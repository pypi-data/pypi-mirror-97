import { FunctionComponent } from 'react';
interface Props {
    width: number;
    height: number;
    initialPosition: number;
    onChange?: (newPosition: number) => void;
    gripThickness?: number;
    gripInnerThickness?: number;
    gripMargin?: number;
}
declare const VSplitter: FunctionComponent<Props>;
export default VSplitter;
