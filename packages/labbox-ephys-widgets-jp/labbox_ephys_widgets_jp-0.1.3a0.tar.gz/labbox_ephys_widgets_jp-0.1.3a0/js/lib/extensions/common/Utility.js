export const isNumber = (x) => {
    return ((x !== null) && (x !== undefined) && (typeof (x) === 'number'));
};
export const isString = (x) => {
    return ((x !== null) && (x !== undefined) && (typeof (x) === 'string'));
};
export const getArrayMin = (array) => {
    return array.reduce((min, current) => min <= current ? min : current, Infinity);
};
export const getArrayMax = (array) => {
    return array.reduce((max, current) => max >= current ? max : current, -Infinity);
};
//# sourceMappingURL=Utility.js.map