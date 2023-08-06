export declare type SortingCuration = {
    labelsByUnit?: {
        [key: string]: string[];
    };
    labelChoices?: string[];
    mergeGroups?: (number[])[];
};
export declare type SortingCurationDispatch = (action: SortingCurationAction) => void;
declare type SetCurationSortingCurationAction = {
    type: 'SetCuration';
    curation: SortingCuration;
};
declare type AddLabelSortingCurationAction = {
    type: 'AddLabel';
    unitId: number;
    label: string;
};
declare type RemoveLabelSortingCurationAction = {
    type: 'RemoveLabel';
    unitId: number;
    label: string;
};
declare type MergeUnitsSortingCurationAction = {
    type: 'MergeUnits';
    unitIds: number[];
};
declare type UnmergeUnitsSortingCurationAction = {
    type: 'UnmergeUnits';
    unitIds: number[];
};
export declare type SortingCurationAction = SetCurationSortingCurationAction | AddLabelSortingCurationAction | RemoveLabelSortingCurationAction | MergeUnitsSortingCurationAction | UnmergeUnitsSortingCurationAction;
export declare const mergeGroupForUnitId: (unitId: number, curation: SortingCuration | undefined) => number[];
export declare const applyMergesToUnit: (unitId: number, curation: SortingCuration | undefined, applyMerges: boolean | undefined) => number | number[];
export declare const isMergeGroupRepresentative: (unitId: number, curation: SortingCuration | undefined) => boolean;
export {};
