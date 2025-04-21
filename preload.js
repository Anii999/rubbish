const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
    detectWaste: (imageData) => ipcRenderer.invoke('detect-waste', imageData)
});
