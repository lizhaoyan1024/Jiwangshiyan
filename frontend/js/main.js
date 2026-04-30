socket.on('step_data', (step) => {
    // 将算法类型传给渲染函数
    const algoType = document.getElementById('algoSelect').value;
    render(step, algoType); 
    
    const stepDesc = document.getElementById('stepDesc');
    if (stepDesc) {
        stepDesc.innerText = `[${step.algorithm}] 步 ${step.step_id}: ${step.description}`;
    }
});

// 提交按钮逻辑
document.getElementById('btnSubmit').onclick = async () => {
    const inputStr = document.getElementById('dataInput').value;
    const algo = document.getElementById('algoSelect').value;
    const currentSpeed = document.getElementById('speedSelect').value;
    const msgEl = document.getElementById('sysMessage');

    try {
        const res = await fetch('http://127.0.0.1:5000/api/submit', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ 
                sid: socket.id, 
                algo_type: algo, 
                input_data: inputStr
            })
        });
        
        const data = await res.json();
        msgEl.innerText = data.message;

        // 如果后端响应成功，激活控制按钮
        if (res.ok) {
            sendControlCommand('set_speed', { speed: currentSpeed });
            document.getElementById('btnStart').disabled = false;
            document.getElementById('btnPause').disabled = true;
            document.getElementById('btnNext').disabled = false;
            document.getElementById('btnPrev').disabled = false;
            msgEl.style.color = "green"; // 提交成功显示绿色
        } else {
            msgEl.style.color = "red";   // 后端报错显示红色
        }

    } catch(e) {
        msgEl.innerText = "连接后端 API 失败，请检查 Flask 是否运行";
        msgEl.style.color = "red";
    }
};

// 点击【自动播放】
document.getElementById('btnStart').onclick = () => {
    sendControlCommand('start');
    document.getElementById('btnStart').disabled = true;  // 自己变灰
    document.getElementById('btnPause').disabled = false; // 暂停变亮
    document.getElementById('btnNext').disabled = true;   // 自动播放时禁用单步
    document.getElementById('btnPrev').disabled = true;
};

// 监听速度下拉菜单的变化
document.getElementById('speedSelect').onchange = (e) => {
    const selectedSpeed = e.target.value; // 获取 "fast", "normal" 或 "slow"
    console.log("正在切换速度为:", selectedSpeed);
    
    // 调用 socket.js 中的函数发送给后端
    sendControlCommand('set_speed', { speed: selectedSpeed });
};

// 点击【暂停】
document.getElementById('btnPause').onclick = () => {
    sendControlCommand('pause');
    document.getElementById('btnStart').disabled = false; // 开始变亮
    document.getElementById('btnPause').disabled = true;  // 自己变灰
    document.getElementById('btnNext').disabled = false;  // 恢复单步
    document.getElementById('btnPrev').disabled = false;
};

document.getElementById('btnNext').onclick = () => sendControlCommand('step_forward');
document.getElementById('btnPrev').onclick = () => sendControlCommand('step_backward');

document.getElementById('btnReset').onclick = () => {
    // 告诉后端重置状态
    sendControlCommand('reset'); 
    // 延迟一小会儿刷新页面，确保后端收到了重置信号
    setTimeout(() => {
        location.reload();
    }, 100);
};