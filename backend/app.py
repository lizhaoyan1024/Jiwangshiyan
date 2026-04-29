# backend/app.py
from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from algorithm_runner import build_heap_steps, build_quick_sort_steps, build_bubble_sort_steps, build_tree_steps
from utils.validator import validate_input

app = Flask(__name__)
CORS(app) 
app.config['SECRET_KEY'] = 'visual_algo_secret'
socketio = SocketIO(app, cors_allowed_origins="*", ping_timeout=10, ping_interval=5) # 强化断线检测

user_sessions = {}

@app.route('/api/submit', methods=['POST'])
def submit_data():
    data = request.json
    raw_data = data.get('input_data')
    sid = data.get('sid')
    algo_type = data.get('algo_type', 'heap')

    # 1. 调用多算法校验
    is_valid, msg, arr = validate_input(raw_data, algo_type)
    if not is_valid:
        return jsonify({"status": "error", "message": msg}), 400

    # 2. 路由到对应的算法执行器
   # 2. 路由到对应的算法执行器 (找到 app.py 中的这段逻辑并替换)
    if algo_type == 'heap':
        steps = build_heap_steps(arr)
    elif algo_type == 'quick_sort':
        steps = build_quick_sort_steps(arr)
    elif algo_type == 'bubble_sort':
        steps = build_bubble_sort_steps(arr)
    elif algo_type == 'binary_tree':
        steps = build_tree_steps(arr)
    else:
        return jsonify({"status": "error", "message": "未知算法类型"}), 400
    # 3. 初始化会话（默认速度为普通 1.2s）
    user_sessions[sid] = {
        'steps': steps, 'index': 0, 'status': 'ready', 'speed': 1.2
    }
    return jsonify({"status": "success", "message": f"{'堆创建' if algo_type=='heap' else '快速排序'} 解析成功"})

@socketio.on('connect')
def handle_connect():
    user_sessions[request.sid] = {'steps': [], 'index': 0, 'status': 'stopped', 'speed': 1.2}
    emit('connected', {'sid': request.sid})

@socketio.on('disconnect')
def handle_disconnect():
    if request.sid in user_sessions:
        del user_sessions[request.sid]

@socketio.on('control')
def handle_control(data):
    sid = request.sid
    command = data.get('command')
    if sid not in user_sessions: return
    session = user_sessions[sid]
    
    if command in ['start', 'resume']:
        session['status'] = 'playing'
        socketio.start_background_task(push_steps, sid)
    elif command == 'pause':
        session['status'] = 'paused'
    elif command == 'reset':
        session['status'] = 'stopped'
        session['index'] = 0
    # --- 扩展功能：单步执行与回溯 ---
    elif command == 'step_forward':
        session['status'] = 'paused' # 强制暂停
        if session['index'] < len(session['steps']):
            socketio.emit('step_data', session['steps'][session['index']], room=sid)
            session['index'] += 1
    elif command == 'step_backward':
        session['status'] = 'paused'
        if session['index'] > 1:
            session['index'] -= 1
            idx_to_show = session['index'] - 1
            socketio.emit('step_data', session['steps'][idx_to_show], room=sid)
    # --- 扩展功能：速度调节 ---
    elif command == 'set_speed':
        speed_map = {'fast': 0.4, 'normal': 1.2, 'slow': 2.5}
        session['speed'] = speed_map.get(data.get('speed', 'normal'), 1.2)

def push_steps(sid):
    session = user_sessions.get(sid)
    while session and session['status'] == 'playing' and session['index'] < len(session['steps']):
        socketio.emit('step_data', session['steps'][session['index']], room=sid)
        session['index'] += 1
        # 使用动态设定的速度
        socketio.sleep(session.get('speed', 1.2))
        
    if session and session['index'] >= len(session['steps']) and session['status'] == 'playing':
        socketio.emit('complete', {'message': '演示已完成'}, room=sid)
        session['status'] = 'stopped'

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000)