import React, { useMemo } from 'react';
import CanvasWidget from '../../common/CanvasWidget';
import { useLayer, useLayers } from '../../common/CanvasWidget/CanvasWidgetLayer';
import { getArrayMax, getArrayMin } from '../../common/Utility';
import createClusterLayer from './clusterLayer';
const IndividualClusterWidget = ({ x, y, width, height, selectedIndex, onSelectedIndexChanged }) => {
    const layerProps = useMemo(() => {
        const xmin = getArrayMin(x);
        const xmax = getArrayMax(x);
        const ymin = getArrayMin(y);
        const ymax = getArrayMax(y);
        const rect = { xmin, xmax, ymin, ymax };
        return {
            x,
            y,
            rect,
            width,
            height,
            selectedIndex,
            onSelectedIndexChanged
        };
    }, [x, y, width, height, onSelectedIndexChanged, selectedIndex]);
    const clusterLayer = useLayer(createClusterLayer, layerProps);
    const layers = useLayers([clusterLayer]);
    return (React.createElement(CanvasWidget, Object.assign({ layers: layers }, { width, height })));
};
export default IndividualClusterWidget;
//# sourceMappingURL=IndividualClusterWidget.js.map