declare type FetchCache<QueryType> = {
    get: (query: QueryType) => any | undefined;
};
declare const useFetchCache: <QueryType>(fetchFunction: (query: QueryType) => Promise<any>) => FetchCache<QueryType>;
export default useFetchCache;
