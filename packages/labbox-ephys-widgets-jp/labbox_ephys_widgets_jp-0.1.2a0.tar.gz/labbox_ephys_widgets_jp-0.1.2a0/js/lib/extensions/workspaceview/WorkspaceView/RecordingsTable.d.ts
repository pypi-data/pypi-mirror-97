import { FunctionComponent } from 'react';
import { Recording, Sorting, WorkspaceRouteDispatch } from "../../pluginInterface";
import './WorkspaceView.css';
interface Props {
    readOnly: boolean;
    recordings: Recording[];
    sortings: Sorting[];
    onDeleteRecordings: (recordingIds: string[]) => void;
    workspaceRouteDispatch: WorkspaceRouteDispatch;
}
declare const RecordingsTable: FunctionComponent<Props>;
export default RecordingsTable;
