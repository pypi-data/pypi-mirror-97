import { IconButton } from '@material-ui/core';
import { CheckCircleOutline, Sync, SyncProblem } from '@material-ui/icons';
import { LabboxProviderContext } from 'labbox';
import React, { useCallback, useContext, useMemo } from 'react';
const ServerStatusControl = ({ color }) => {
    const { websocketStatus, onReconnectWebsocket } = useContext(LabboxProviderContext);
    const { icon, title } = useMemo(() => {
        switch (websocketStatus) {
            case 'waiting': {
                return { icon: React.createElement(Sync, { style: { color: 'blue' } }), title: 'Loading...' };
            }
            case 'connected': {
                return { icon: React.createElement(CheckCircleOutline, { style: { color } }), title: 'Connected' };
            }
            case 'disconnected': {
                return { icon: React.createElement(SyncProblem, { style: { color: 'red' } }), title: `Disconnected from server. Click to attempt reconnect.` };
            }
            default: {
                throw Error('Unexpected.');
            }
        }
    }, [websocketStatus, color]);
    const handleClick = useCallback(() => {
        if (websocketStatus === 'disconnected') {
            onReconnectWebsocket();
        }
    }, [websocketStatus, onReconnectWebsocket]);
    return (React.createElement(IconButton, { title: title, onClick: handleClick }, icon));
};
export default ServerStatusControl;
//# sourceMappingURL=ServerStatusControl.js.map