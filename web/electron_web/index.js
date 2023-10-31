const { app, BrowserWindow, ipcMain } = require('electron')
const { program } = require('commander');
const path = require('path');
const { exec } = require('child_process');

program
	.option('-p, --webport <webport>', '输入web端口')
	.option('-s, --serverprocess <serverprocess>', '输入进程数字');

let serverprocess = 0

const createWindow = () => {
	const win = new BrowserWindow({
		width: 888,
		height: 750,
		resizable: false, // 禁止窗口大小调整
		 webPreferences: {
			 preload: path.join(__dirname, 'preload.js'),
			 contextIsolation: true
		},
	})
	win.setMenu(null)
	win.loadFile('index.html')
	program.parse();
	const proargs = program.opts()
	serverprocess = proargs.serverprocess
	win.webContents.send('process-args', {
		webport: proargs.webport,
		serverprocess: proargs.serverprocess
	});
}

app.whenReady().then(() => {
	createWindow()
})
app.on('quit', (event, exitCode) => {
	if (serverprocess !== 0) {
		exec(`taskkill /F /PID ${Number(serverprocess)}`, (error, stdout, stderr) => {
		if (error) {
			console.error(`杀死进程失败: ${error.message}`);
			return;
		}
		console.log(`进程已成功杀死: ${serverprocess}`);
	});
	}
})
