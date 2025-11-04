# Keylogger and Keylogger Detector

## Overview
This project implements a basic keylogger and a keylogger detector. The aim is to demonstrate how keyloggers can be built and infiltrated into systems using various techniques, as well as how they can be detected and removed.

## Objectives
1. Build a basic keylogger.
2. Infiltrate the keylogger into a system using malicious emails, phishing, and steganography techniques.
3. Detect and remove the keylogger from the infected system.

## Steps

### 1. Building the Keylogger
- Implement the keylogger using Python and the `pynput` library.
- Package the keylogger as a standalone executable using PyInstaller.
- Ensure the keylogger can run silently in the background, logging keystrokes to a file.

### 2. Infiltrating the Keylogger
- **Malicious Emails**: Craft convincing phishing emails to trick users into running the keylogger executable.
- **Phishing**: Create fake login pages or attachments that deliver the keylogger when interacted with.
- **Steganography**: Hide the keylogger executable within innocuous-looking files (e.g., images or documents) to evade detection.

### 3. Detecting and Removing the Keylogger
- **Monitoring System Processes**: Identify and analyze unfamiliar or suspicious processes running in the background.
- **File System Monitoring**: Look for unexpected files or changes in system directories.
- **Registry and Startup Item Checks**: Inspect the registry and startup items for suspicious entries (Windows).
- **Network Traffic Analysis**: Check for unusual network activity that might indicate keylogger data being sent out.
- **Removal**: Terminate the keylogger process and delete associated files and registry entries.

## Getting Started
### Prerequisites
- Python 3.x
- `pynput` library
- PyInstaller


## Flask Server
The logging server uses Flask with an SQLite database to store keystrokes. Each user must register with a username and password using the `/register` endpoint. All routes that accept or display logs (`/log`, `/logs/<user>`, `/view_logs/<user>` and related endpoints) are protected with HTTP basic authentication. The database is created automatically as `logs.db` in the `flask-server` directory.
