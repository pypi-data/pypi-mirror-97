// LABBOX-EXTENSION: electrodegeometry
// LABBOX-EXTENSION-TAGS: jupyter
import GrainIcon from '@material-ui/icons/Grain';
import React, { useMemo } from 'react';
import { useRecordingInfo } from '../common/useRecordingInfo';
import ElectrodeGeometryWidget from './ElectrodeGeometryWidget/ElectrodeGeometryWidget';
const zipElectrodes = (locations, ids) => {
    if (locations && ids && ids.length !== locations.length)
        throw Error('Electrode ID count does not match location count.');
    return ids.map((x, index) => {
        const loc = locations[index];
        return { label: x + '', id: x, x: loc[0], y: loc[1] };
    });
};
const ElectrodeGeometryRecordingView = ({ recording, width, height, selection, selectionDispatch }) => {
    const ri = useRecordingInfo(recording.recordingObject);
    const visibleElectrodeIds = selection.visibleElectrodeIds;
    const electrodes = useMemo(() => (ri ? zipElectrodes(ri.geom, ri.channel_ids) : []).filter(a => ((!visibleElectrodeIds) || (visibleElectrodeIds.includes(a.id)))), [ri, visibleElectrodeIds]);
    // const handleSelectedElectrodeIdsChanged = useCallback((x: number[]) => {
    //     selectionDispatch({type: 'SetSelectedElectrodeIds', selectedElectrodeIds: x})
    // }, [selectionDispatch])
    // const selectedElectrodeIds = useMemo(() => (selection.selectedElectrodeIds || []), [selection.selectedElectrodeIds])
    // const [selectedElectrodeIds, setSelectedElectrodeIds] = useState<number[]>([]);
    if (!ri) {
        return (React.createElement("div", null, "No recording info found for recording."));
    }
    return (React.createElement(ElectrodeGeometryWidget, { electrodes: electrodes, selection: selection, selectionDispatch: selectionDispatch, width: width || 350, height: height || 150 }));
};
const ElectrodeGeometrySortingView = ({ recording, recordingInfo, calculationPool, width, height, selection, selectionDispatch }) => {
    return (React.createElement(ElectrodeGeometryRecordingView, Object.assign({}, { recording, recordingInfo, calculationPool, width, height, selection, selectionDispatch })));
};
export function activate(context) {
    context.registerPlugin({
        type: 'RecordingView',
        name: 'ElectrodeGeometryRecordingView',
        label: 'Electrode geometry',
        priority: 50,
        defaultExpanded: false,
        component: ElectrodeGeometryRecordingView,
        singleton: true,
        icon: React.createElement(GrainIcon, null)
    });
    context.registerPlugin({
        type: 'SortingView',
        name: 'ElectrodeGeometrySortingView',
        label: 'Electrode geometry',
        priority: 50,
        component: ElectrodeGeometrySortingView,
        singleton: true,
        icon: React.createElement(GrainIcon, null)
    });
}
//# sourceMappingURL=electrodegeometry.js.map