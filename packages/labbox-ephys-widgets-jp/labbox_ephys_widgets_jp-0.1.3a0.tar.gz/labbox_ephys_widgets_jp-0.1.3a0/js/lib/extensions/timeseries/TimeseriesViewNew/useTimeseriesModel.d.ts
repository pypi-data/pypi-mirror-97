import { RecordingInfo } from "../../pluginInterface";
export declare type TimeseriesData = {
    getChannelData: (ch: number, t1: number, t2: number, ds_factor: number) => number[];
    requestChannelData: (ch: number, t1: number, t2: number, ds_factor: number) => void;
    numChannels: () => number;
    numTimepoints: () => number;
    getSampleRate: () => number;
};
declare const useTimeseriesData: (recordingObject: any, recordingInfo: RecordingInfo) => TimeseriesData | null;
export default useTimeseriesData;
