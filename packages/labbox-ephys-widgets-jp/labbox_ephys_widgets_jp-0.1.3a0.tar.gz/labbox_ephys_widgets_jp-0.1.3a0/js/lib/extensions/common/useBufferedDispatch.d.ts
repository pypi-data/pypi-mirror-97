declare const useBufferedDispatch: <State, Action>(reducer: (s: State, a: Action) => State, state: State, setState: (s: State) => void, t: number) => [State, (a: Action) => void];
export default useBufferedDispatch;
