import { useEffect, useMemo, useReducer, useRef } from "react";
export const dummyAppendOnlyLog = {
    appendMessages: (messages) => { },
    allMessages: () => ([]),
    onMessages: (callback) => { }
};
export const useFeedReducer = (reducer, initialState, subfeed) => {
    const [state, stateDispatch] = useReducer(reducer, initialState);
    const ref = useRef({ messageCount: 0 });
    useEffect(() => {
        if (subfeed) {
            // subfeed.allMessages().forEach(msg => {
            //   stateDispatch(msg)
            // })
            subfeed.onMessages((position, msgs) => {
                if (position < ref.current.messageCount)
                    msgs = msgs.slice(ref.current.messageCount - position);
                if (msgs.length > 0) {
                    msgs.forEach(msg => stateDispatch(msg));
                    ref.current.messageCount += msgs.length;
                }
            });
        }
    }, [subfeed]);
    const newDispatch = useMemo(() => ((a) => {
        if (subfeed) {
            subfeed.appendMessages([a]);
        }
        else {
            stateDispatch(a);
        }
    }), [subfeed]);
    return [state, newDispatch];
};
//# sourceMappingURL=useFeedReducer.js.map