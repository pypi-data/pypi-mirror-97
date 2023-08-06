import React from 'react';
import ElectrodeGeometry from './ElectrodeGeometry';
const ElectrodeGeometryTest = (props) => {
    const electrodes = [[20, 20], [40, 40], [60, 100], [80, 120]].map((coords, ii) => ({
        id: ii,
        label: ii + '',
        x: coords[0],
        y: coords[1]
    }));
    return (React.createElement(ElectrodeGeometry, { electrodes: electrodes }));
};
export default ElectrodeGeometryTest;
//# sourceMappingURL=ElectrodeGeometryTest.js.map