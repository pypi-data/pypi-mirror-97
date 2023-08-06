import { HitherInterface } from 'labbox';
import { Recording, RecordingInfo } from "../pluginInterface";
export declare const getRecordingInfo: (a: {
    recordingObject: any;
    hither: HitherInterface;
}) => Promise<RecordingInfo>;
export declare const useRecordingInfo: (recordingObject: any) => RecordingInfo | undefined;
export declare const useRecordingInfos: (recordings: Recording[]) => {
    [key: string]: RecordingInfo;
};
