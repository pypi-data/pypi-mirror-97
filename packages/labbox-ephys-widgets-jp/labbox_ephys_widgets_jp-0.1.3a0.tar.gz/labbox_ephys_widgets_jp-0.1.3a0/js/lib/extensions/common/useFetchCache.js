import objectHash from 'object-hash';
import { useEffect, useMemo, useReducer, useRef, useState } from "react";
const initialFetchCacheState = {
    data: {},
    activeFetches: {}
};
const fetchCacheReducer = (state, action) => {
    switch (action.type) {
        case 'clear': {
            return initialFetchCacheState;
        }
        case 'startFetch': {
            return Object.assign(Object.assign({}, state), { activeFetches: Object.assign(Object.assign({}, state.activeFetches), { [action.queryHash]: true }) });
        }
        case 'setData': {
            return Object.assign(Object.assign({}, state), { data: Object.assign(Object.assign({}, state.data), { [action.queryHash]: action.data }), activeFetches: Object.assign(Object.assign({}, state.activeFetches), { [action.queryHash]: false }) });
        }
        default: {
            throw Error('Unexpected action in fetchCacheReducer');
        }
    }
};
const queryHash = (query) => {
    return objectHash(query);
};
const useFetchCache = (fetchFunction) => {
    const [count, setCount] = useState(0);
    if (count < 0)
        console.info(count); // just suppress the unused warning (will never print)
    const prevFetchFunction = useRef(fetchFunction);
    const [state, dispatch] = useReducer(fetchCacheReducer, initialFetchCacheState);
    const queriesToFetch = useRef({});
    useEffect(() => {
        // clear whenever fetchFunction has Changed
        if (fetchFunction !== prevFetchFunction.current) {
            prevFetchFunction.current = fetchFunction;
            dispatch({ type: 'clear' });
        }
    }, [fetchFunction]);
    const get = useMemo(() => ((query) => {
        const h = queryHash(query);
        const v = state.data[h];
        if (v === undefined) {
            queriesToFetch.current[h] = query;
            setCount((c) => (c + 1)); // make sure we trigger a state change so we go to the useEffect below
        }
        return v;
    }), [state.data]);
    const fetch = useMemo(() => ((query) => {
        const h = queryHash(query);
        const val = state.data[h];
        if (val !== undefined)
            return;
        if (state.activeFetches[h])
            return;
        dispatch({ type: 'startFetch', queryHash: h });
        fetchFunction(query).then((data) => {
            dispatch({ type: 'setData', queryHash: h, data });
        }).catch((err) => {
            console.warn(err);
            console.warn('Problem fetching data', query);
            // note: we intentionally do not unset the active fetch here
        });
    }), [state.data, state.activeFetches, fetchFunction]);
    useEffect(() => {
        const keys = Object.keys(queriesToFetch.current);
        if (keys.length === 0)
            return;
        for (let k of keys) {
            fetch(queriesToFetch.current[k]);
        }
        queriesToFetch.current = {};
    });
    return useMemo(() => ({
        get
    }), [get]);
};
export default useFetchCache;
//# sourceMappingURL=useFetchCache.js.map