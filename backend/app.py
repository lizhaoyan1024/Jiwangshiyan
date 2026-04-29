from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from algorithm_runner import build_heap_steps
from utils.validator import validate_input
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'visual_algo_secret'
# 集成WebSocket扩展，配置跨域支持 [cite: 56]
socketio = SocketIO(app, cors_allowed_origins="*")

user_sessions = {} # 用户会话管理机制 [cite: 58]

@app.route('/api/submit', methods=['POST'])
def submit_data():
    """定义HTTP POST接口，用于接收前端提交的输入数据及算法类型 [cite: 55]"""
    data = request.json
    raw_data = data.get('input_data')
    sid = data.get('sid')

    is_valid, msg, arr = validate_input(raw_data)
    if not is_valid:
        return jsonify({"status": "error", "message": msg}), 400

    # 校验通过后调用对应算法执行器，生成步骤数据 [cite: 55]
    steps = build_heap_steps(arr)
    user_sessions[sid] = {'steps': steps, 'index': 0, 'status': 'ready'}
    
    return jsonify({"status": "success", "message": "数据提交成功，开始演示"})

@socketio.on('connect')
def handle_connect():
    """实现WebSocket连接建立的监听逻辑 [cite: 56]"""
    print(f"Client connected: {request.sid}")
    emit('connected', {'sid': request.sid})

@socketio.on('control')
def handle_control(data):
    """前端指令（如开始演示、暂停）的接收逻辑 [cite: 56]"""
    sid = data.get('sid')
    command = data.get('command')
    
    if sid in user_sessions:
        session = user_sessions[sid]
        if command == 'start' or command == 'resume':
            session['status'] = 'playing'
            socketio.start_background_task(push_steps, sid)
        elif command == 'pause':
            session['status'] = 'paused'
        elif command == 'reset':
            session['status'] = 'stopped'
            session['index'] = 0

def push_steps(sid):
    """逐一步通过WebSocket推送给前端 [cite: 57]"""
    session = user_sessions.get(sid)
    while session and session['status'] == 'playing' and session['index'] < len(session['steps']):
        step_data = session['steps'][session['index']]
        socketio.emit('step_data', step_data, room=sid)
        session['index'] += 1
        socketio.sleep(1.5)
        
    if session and session['index'] >= len(session['steps']) and session['status'] == 'playing':
        socketio.emit('complete', {'message': '演示完成'}, room=sid)
        session['status'] = 'stopped'

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000)