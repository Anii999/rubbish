const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const { execFile } = require('child_process');

let mainWindow;

function createWindow() {
    mainWindow = new BrowserWindow({
        width: 1200,
        height: 800,
        webPreferences: {
            preload: path.join(__dirname, 'preload.js'),
            nodeIntegration: false,
            contextIsolation: true
        }
    });

    mainWindow.loadFile('detection.html');

    mainWindow.on('closed', function () {
        mainWindow = null;
    });
}

app.whenReady().then(() => {
    createWindow();

    app.on('activate', function () {
        if (BrowserWindow.getAllWindows().length === 0) createWindow();
    });
});

app.on('window-all-closed', function () {
    if (process.platform !== 'darwin') app.quit();
});

// EXE调用处理
ipcMain.handle('detect-waste', (event, imageData) => {
    return new Promise((resolve, reject) => {
        // 提取base64数据
        const base64Data = imageData.replace(/^data:image\/\w+;base64,/, '');
        const buffer = Buffer.from(base64Data, 'base64');

        // 临时保存图片文件
        const fs = require('fs');
        const tempFilePath = path.join(__dirname, 'temp_input.jpg');
        fs.writeFileSync(tempFilePath, buffer);

        // 调用EXE程序
        const exePath = path.join(__dirname, 'exe.win-amd64-3.13', '主界面.exe');
        const outputPath = path.join(__dirname, 'temp_output.json');

        execFile(exePath, [tempFilePath, outputPath], (error, stdout, stderr) => {
            if (error) {
                console.error('EXE执行错误:', error);
                reject(error);
                return;
            }

            // 读取EXE输出结果
            try {
                const result = JSON.parse(fs.readFileSync(outputPath, 'utf-8'));
                resolve(result);
            } catch (parseError) {
                console.error('结果解析错误:', parseError);
                reject(parseError);
            }

            // 清理临时文件
            fs.unlinkSync(tempFilePath);
            fs.unlinkSync(outputPath);
        });
    });
});
