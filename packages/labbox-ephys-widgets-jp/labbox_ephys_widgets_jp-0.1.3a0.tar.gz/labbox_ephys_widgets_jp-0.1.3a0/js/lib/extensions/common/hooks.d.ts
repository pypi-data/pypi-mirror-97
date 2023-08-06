declare type CleanupFunction = () => void;
export declare const useOnce: (fun: () => void | CleanupFunction) => void;
export declare const useCheckForChanges: (label: string, x: {
    [key: string]: any;
}) => void;
export {};
