function updateStatus(status) {
    const statusElem = document.getElementById('status');
    statusElem.textContent = status;
}

const startBtn = document.getElementById('startBtn');
const stopBtn = document.getElementById('stopBtn');

startBtn.addEventListener('click', () => {
    const xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                // 成功時は自動的にSSEでの更新も行われるため、ここでは何もしない
            } else {
                alert('録画の開始に失敗しました');
            }
        }
    };
    xhr.open('POST', '/video/start_recording', true);
    xhr.send();
});

stopBtn.addEventListener('click', () => {
    const xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                // 成功時は自動的にSSEでの更新も行われるため、ここでは何もしない
            } else {
                alert('録画の停止に失敗しました');
            }
        }
    };
    xhr.open('POST', '/video/stop_recording', true);
    xhr.send();
});

// SSEを使用して状態をリアルタイムに更新
const eventSource = new EventSource('/video/stream_status');
eventSource.onmessage = function (event) {
    const status = event.data;
    updateStatus(status);
};
