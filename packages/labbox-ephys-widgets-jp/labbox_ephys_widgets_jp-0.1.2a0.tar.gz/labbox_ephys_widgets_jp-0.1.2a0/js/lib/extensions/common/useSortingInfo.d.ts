import { Sorting, SortingInfo } from "../pluginInterface";
export declare const useSortingInfo: (sortingObject: any, recordingObject: any) => SortingInfo | undefined;
export declare const useSortingInfos: (sortings: Sorting[]) => {
    [key: string]: SortingInfo;
};
