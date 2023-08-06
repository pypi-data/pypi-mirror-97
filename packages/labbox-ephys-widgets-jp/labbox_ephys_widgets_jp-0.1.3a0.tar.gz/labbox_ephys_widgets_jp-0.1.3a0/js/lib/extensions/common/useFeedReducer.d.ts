export interface AppendOnlyLog {
    appendMessages: (messages: any[]) => void;
    allMessages: () => any[];
    onMessages: (callback: (position: number, messages: any[]) => void) => void;
}
export declare const dummyAppendOnlyLog: {
    appendMessages: (messages: any[]) => void;
    allMessages: () => never[];
    onMessages: (callback: (position: number, messages: any[]) => void) => void;
};
export declare const useFeedReducer: <State, Action>(reducer: (s: State, a: Action) => State, initialState: State, subfeed: AppendOnlyLog | null) => [State, (a: Action) => void];
