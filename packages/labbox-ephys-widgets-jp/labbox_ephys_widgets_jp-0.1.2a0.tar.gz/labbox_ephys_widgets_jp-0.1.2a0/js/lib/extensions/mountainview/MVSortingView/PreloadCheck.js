var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
import { createCalculationPool, HitherContext } from 'labbox';
import React, { Fragment, useContext, useEffect, useMemo, useRef, useState } from 'react';
const calculationPool = createCalculationPool({ maxSimultaneous: 6 });
const PreloadCheck = ({ recording, sorting, children, width, height }) => {
    const hither = useContext(HitherContext);
    const sortingObject = sorting.sortingObject;
    const recordingObject = recording.recordingObject;
    const [error, setError] = useState(null);
    const [status, setStatus] = useState('waiting');
    const [message, setMessage] = useState('');
    const runningState = useRef({ sortingObject: sorting.sortingObject, recordingObject: recording.recordingObject });
    const matchesRunningState = useMemo(() => ((x) => ((runningState.current.sortingObject === x.sortingObject) && (runningState.current.recordingObject === x.recordingObject))), []);
    useEffect(() => {
        if (status === 'waiting') {
            runningState.current = { recordingObject, sortingObject };
            setStatus('running');
            (() => __awaiter(void 0, void 0, void 0, function* () {
                try {
                    setMessage('Checking sorting data...');
                    const result1 = yield hither.createHitherJob('preload_check_sorting_downloaded', { sorting_object: sortingObject }, { useClientCache: false, calculationPool }).wait();
                    if (!matchesRunningState({ recordingObject, sortingObject }))
                        return;
                    if (!result1.isLocal) {
                        setMessage('Downloading sorting...');
                        const result2 = yield hither.createHitherJob('preload_download_sorting', { sorting_object: sortingObject }, { useClientCache: false, calculationPool }).wait();
                        if (!matchesRunningState({ recordingObject, sortingObject }))
                            return;
                        if (!result2.success) {
                            setError(new Error('Unable to download sorting.'));
                            return;
                        }
                    }
                    setMessage('Checking recording data...');
                    const result3 = yield hither.createHitherJob('preload_check_recording_downloaded', { recording_object: recordingObject }, { useClientCache: false, calculationPool }).wait();
                    if (!matchesRunningState({ recordingObject, sortingObject }))
                        return;
                    if (!result3.isLocal) {
                        setMessage('Downloading recording...');
                        const result4 = yield hither.createHitherJob('preload_download_recording', { recording_object: recordingObject }, { useClientCache: false, calculationPool }).wait();
                        if (!matchesRunningState({ recordingObject, sortingObject }))
                            return;
                        if (!result4.success) {
                            setError(new Error('Unable to download recording.'));
                            return;
                        }
                    }
                    setMessage('Extracting snippets...');
                    const result5 = yield hither.createHitherJob('preload_extract_snippets', { recording_object: recordingObject, sorting_object: sortingObject }, { useClientCache: false, calculationPool }).wait();
                    if (!matchesRunningState({ recordingObject, sortingObject }))
                        return;
                    if (!result5) {
                        setError(new Error('Problem extracting snippets'));
                        return;
                    }
                    setStatus('finished');
                }
                catch (err) {
                    setError(err);
                }
            }))();
        }
        else {
            if (!matchesRunningState({ recordingObject, sortingObject })) {
                setStatus('waiting');
            }
        }
    }, [sortingObject, recordingObject, status, matchesRunningState, hither]);
    const child = useMemo(() => {
        return React.cloneElement(children, {
            preloadStatus: status
        });
    }, [children, status]);
    // This is important for when the bandpass filter changes so that we don't start calculating things prior to doing the preloading (e.g. snippets extraction)
    const [lastValidChild, setLastValidChild] = useState(null);
    useEffect(() => {
        if ((status === 'finished') && (matchesRunningState({ recordingObject, sortingObject })))
            setLastValidChild(child);
    }, [child, status, recordingObject, sortingObject, matchesRunningState]);
    return (React.createElement(Fragment, null,
        React.createElement(BlockInteraction, Object.assign({ block: status !== 'finished' }, { width, height }, { message: error ? `Error: ${error.message}` : message })),
        lastValidChild || child));
};
const BlockInteraction = ({ width, height, block, message }) => {
    if (block) {
        return (React.createElement("div", { className: "BlockInteraction", style: { position: 'absolute', width, height, backgroundColor: 'gray', opacity: 0.5, zIndex: 99999 } },
            React.createElement("div", { style: { backgroundColor: 'blue', color: 'white', fontSize: 20 } }, message)));
    }
    else {
        return React.createElement("div", { className: "BlockInteraction" });
    }
};
export default PreloadCheck;
//# sourceMappingURL=PreloadCheck.js.map