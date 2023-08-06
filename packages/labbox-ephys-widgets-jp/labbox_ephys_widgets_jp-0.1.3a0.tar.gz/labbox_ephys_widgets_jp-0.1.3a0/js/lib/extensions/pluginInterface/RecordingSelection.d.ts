import { Reducer } from "react";
export interface RecordingSelection {
    selectedElectrodeIds?: number[];
    visibleElectrodeIds?: number[];
    currentTimepoint?: number;
    timeRange?: {
        min: number;
        max: number;
    } | null;
    ampScaleFactor?: number;
    animation?: {
        currentTimepointVelocity: number;
    };
    waveformsMode?: 'geom' | 'vertical';
}
export declare const useRecordingAnimation: (selection: RecordingSelection, selectionDispatch: RecordingSelectionDispatch) => void;
export declare const sleepMsec: (m: number) => Promise<unknown>;
export declare type RecordingSelectionDispatch = (action: RecordingSelectionAction) => void;
declare type SetRecordingSelectionRecordingSelectionAction = {
    type: 'SetRecordingSelection';
    recordingSelection: RecordingSelection;
};
declare type SetSelectedElectrodeIdsRecordingSelectionAction = {
    type: 'SetSelectedElectrodeIds';
    selectedElectrodeIds: number[];
};
declare type SetVisibleElectrodeIdsRecordingSelectionAction = {
    type: 'SetVisibleElectrodeIds';
    visibleElectrodeIds: number[];
};
declare type SetCurrentTimepointRecordingSelectionAction = {
    type: 'SetCurrentTimepoint';
    currentTimepoint: number | null;
    ensureInRange?: boolean;
};
declare type SetTimeRangeRecordingSelectionAction = {
    type: 'SetTimeRange';
    timeRange: {
        min: number;
        max: number;
    } | null;
};
declare type ZoomTimeRangeRecordingSelectionAction = {
    type: 'ZoomTimeRange';
    factor?: number;
    direction?: 'in' | 'out';
};
declare type SetAmpScaleFactorRecordingSelectionAction = {
    type: 'SetAmpScaleFactor';
    ampScaleFactor: number;
};
declare type ScaleAmpScaleFactorRecordingSelectionAction = {
    type: 'ScaleAmpScaleFactor';
    multiplier?: number;
    direction?: 'up' | 'down';
};
declare type SetCurrentTimepointVelocityRecordingSelectionAction = {
    type: 'SetCurrentTimepointVelocity';
    velocity: number;
};
declare type SetWaveformsModeRecordingSelectionAction = {
    type: 'SetWaveformsMode';
    waveformsMode: 'geom' | 'vertical';
};
declare type SetRecordingSelectionAction = {
    type: 'Set';
    state: RecordingSelection;
};
export declare type RecordingSelectionAction = SetRecordingSelectionRecordingSelectionAction | SetSelectedElectrodeIdsRecordingSelectionAction | SetVisibleElectrodeIdsRecordingSelectionAction | SetCurrentTimepointRecordingSelectionAction | SetTimeRangeRecordingSelectionAction | ZoomTimeRangeRecordingSelectionAction | SetAmpScaleFactorRecordingSelectionAction | ScaleAmpScaleFactorRecordingSelectionAction | SetCurrentTimepointVelocityRecordingSelectionAction | SetWaveformsModeRecordingSelectionAction | SetRecordingSelectionAction;
export declare const recordingSelectionReducer: Reducer<RecordingSelection, RecordingSelectionAction>;
export {};
