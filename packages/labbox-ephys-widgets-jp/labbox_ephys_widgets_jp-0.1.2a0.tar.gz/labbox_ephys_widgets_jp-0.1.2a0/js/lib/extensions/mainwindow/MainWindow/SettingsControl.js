import { IconButton } from '@material-ui/core';
import { Settings } from '@material-ui/icons';
import React, { useCallback, useMemo } from 'react';
const SettingsControl = ({ onOpenSettings, color }) => {
    const { icon, title } = useMemo(() => {
        return { icon: React.createElement(Settings, null), title: 'Open settings' };
    }, []);
    const handleClick = useCallback(() => {
        onOpenSettings();
    }, [onOpenSettings]);
    return (React.createElement(IconButton, { style: { color }, title: title, onClick: handleClick }, icon));
};
export default SettingsControl;
//# sourceMappingURL=SettingsControl.js.map