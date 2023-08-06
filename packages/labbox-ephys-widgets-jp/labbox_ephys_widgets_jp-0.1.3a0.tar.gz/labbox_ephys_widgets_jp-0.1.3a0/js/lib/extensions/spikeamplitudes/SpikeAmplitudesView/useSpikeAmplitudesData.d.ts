export declare type SpikeAmplitudesData = {
    getSpikeAmplitudes: (unitId: number | number[]) => {
        timepoints: number[];
        amplitudes: number[];
        minAmp: number;
        maxAmp: number;
    } | undefined | null;
};
declare const useSpikeAmplitudesData: (recordingObject: any, sortingObject: any) => SpikeAmplitudesData | null;
export default useSpikeAmplitudesData;
