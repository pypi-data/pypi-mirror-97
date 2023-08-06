declare const sortByPriority: <T extends {
    label: string;
    priority?: number | undefined;
}>(x: {
    [key: string]: T;
} | T[]) => T[];
export default sortByPriority;
