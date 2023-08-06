import { FunctionComponent } from 'react';
interface Props {
    width: number;
    height: number;
    initialPosition: number;
    positionFromRight?: boolean;
    onChange?: (newPosition: number) => void;
    gripThickness?: number;
    gripInnerThickness?: number;
    gripMargin?: number;
    adjustable?: boolean;
}
declare const Splitter: FunctionComponent<Props>;
export default Splitter;
