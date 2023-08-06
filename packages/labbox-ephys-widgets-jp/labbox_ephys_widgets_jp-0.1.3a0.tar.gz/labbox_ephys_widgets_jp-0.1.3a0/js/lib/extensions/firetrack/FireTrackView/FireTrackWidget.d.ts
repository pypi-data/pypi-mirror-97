import { FunctionComponent } from 'react';
import { Recording, SortingSelection } from "../../pluginInterface";
import { TimeseriesData } from "../../timeseries/TimeseriesViewNew/useTimeseriesModel";
declare const FireTrackWidget: FunctionComponent<{
    recording: Recording;
    timeseriesData: TimeseriesData | null;
    selection: SortingSelection;
    width: number;
    height: number;
}>;
export default FireTrackWidget;
