const isArray = (x) => {
    return (Array.isArray(x));
};
const sortByPriority = (x) => {
    if (isArray(x)) {
        return x.sort((a, b) => (a.priority === b.priority ? (((a.label || '') < (b.label || '')) ? -1 : ((a.label || '') > (b.label || '')) ? 1 : 0) : ((b.priority || 0) - (a.priority || 0))));
    }
    else {
        return sortByPriority(Object.values(x));
    }
};
export default sortByPriority;
//# sourceMappingURL=sortByPriority.js.map