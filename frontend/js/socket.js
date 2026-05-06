/**
 * socket.js - 专门负责与后端进行 WebSocket 通信的模块
 */

// 1. 初始化连接 (指向 Flask 后端地址)
const socket = io('http://123.249.30.251:5000');

// 2. 状态监控：连接成功
socket.on('connect', () => {
    const statusEl = document.getElementById('wsStatus');
    if (statusEl) {
        statusEl.innerText = '🟢 WebSocket 已连接';
        statusEl.style.color = 'green';
    }
    console.log("WebSocket connected, ID:", socket.id);
});

// 3. 状态监控：断开连接
socket.on('disconnect', () => {
    const statusEl = document.getElementById('wsStatus');
    if (statusEl) {
        statusEl.innerText = '🔴 WebSocket 已断开 (重连中...)';
        statusEl.style.color = 'red';
    }
});

/**
 * 通用命令发送函数
 * @param {string} cmd - 指令名称 (start, pause, step_forward 等)
 * @param {object} params - 携带的参数 (如 speed)
 */
function sendControlCommand(cmd, params = {}) {
    socket.emit('control', { command: cmd, ...params });
}