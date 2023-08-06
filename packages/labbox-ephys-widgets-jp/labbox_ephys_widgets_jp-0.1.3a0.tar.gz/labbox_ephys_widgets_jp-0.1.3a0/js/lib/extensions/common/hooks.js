import { useEffect, useRef, useState } from "react";
// Call the function only once after the first component render
export const useOnce = (fun) => {
    // We use a ref here so as to avoid compiler warning of passing in empty dependency array to useEffect
    // The function fun will be different with each call, but the functionality of fun should remain the same. We use a ref to capture just the first fun passed in.
    const state = useRef(fun);
    useEffect(() => {
        return state.current();
    }, []); // this would give a warning if we were passing fun in directly
};
// For debugging
export const useCheckForChanges = (label, x) => {
    const [previous, setPrevious] = useState(null);
    let somethingChanged = false;
    if (previous) {
        for (let k in previous) {
            if (x[k] !== previous[k]) {
                somethingChanged = true;
                console.info(`CHANGED: ${label}: ${k}`);
            }
        }
    }
    else {
        somethingChanged = true;
    }
    if (somethingChanged)
        setPrevious(x);
};
//# sourceMappingURL=hooks.js.map