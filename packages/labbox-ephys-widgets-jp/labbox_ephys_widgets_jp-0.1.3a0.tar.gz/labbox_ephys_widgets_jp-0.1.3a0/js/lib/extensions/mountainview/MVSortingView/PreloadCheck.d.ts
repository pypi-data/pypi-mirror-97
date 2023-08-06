import React, { FunctionComponent } from 'react';
import { Recording, Sorting } from "../../pluginInterface";
interface ChildProps {
    preloadStatus?: 'waiting' | 'running' | 'finished';
}
declare type Props = {
    sorting: Sorting;
    recording: Recording;
    children: React.ReactElement<ChildProps>;
    width: number;
    height: number;
};
declare const PreloadCheck: FunctionComponent<Props>;
export default PreloadCheck;
