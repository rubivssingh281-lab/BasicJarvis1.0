# Xeno - Advanced Voice Assistant

An AI-powered desktop voice assistant built with Python, Tkinter, Speech Recognition, Text-to-Speech, System Automation, and Local LLM integration using Ollama.

---

# Features

## Voice Recognition

* Continuous voice listening mode
* Speech-to-text using Google Speech Recognition
* Ambient noise adjustment
* Real-time voice visualization

## Text-to-Speech

* Natural voice responses
* Adjustable speech rate
* Multi-voice support

## Application Control

### Browser Control

* Open Chrome
* Open Brave Browser
* New tab
* Close tab
* Next tab
* Previous tab
* Refresh page
* Open bookmarks
* Open history
* Open downloads
* Open incognito mode

### Notepad Control

* Save file
* Open file
* Create new file
* Copy
* Paste
* Cut
* Undo
* Find
* Replace

### File Explorer Control

* Create new folder
* Rename files
* Copy/Paste
* Delete
* View properties
* Change folder views

### VLC Media Control

* Play/Pause
* Stop
* Next track
* Previous track
* Volume control
* Fullscreen
* Mute

---

# System Controls

* Shutdown computer
* Restart computer
* Sleep computer
* Lock screen
* Open Task Manager
* Show system information

---

# File Management

Create folders using voice commands.

Example:

Create folder Projects

Creates:

Desktop/Projects

Create files using voice commands.

Example:

Create file notes.txt

Creates:

Desktop/notes.txt

---

# VS Code Integration

Open folders directly in Visual Studio Code.

Examples:

Open folder D:\Projects in VS Code

Open file main.py in VS Code

---

# Jupyter Notebook Integration

Open notebooks directly.

Examples:

Open notebook machine_learning.ipynb

Open notebook D:\AI\training.ipynb

---

# Terminal Integration

Open terminal windows.

Examples:

Open terminal

Open command prompt

Open PowerShell

Execute terminal commands:

Run command python app.py

Run command git status

Run command pip install requests

---

# Brave Browser Integration

Commands:

Open Brave

New tab in Brave

Open Brave incognito

Close Brave

---

# Mathematical Calculations

Supports:

* Addition
* Subtraction
* Multiplication
* Division
* Powers
* Modulus
* Trigonometry
* Logarithms
* Square roots

Examples:

Calculate 15 plus 7

Calculate 100 divided by 4

Calculate square root of 64

Calculate sin of 30 degrees

Calculate cos of pi radians

Calculate 2 to the power of 10

---

# Screenshot Utility

Command:

Take screenshot

Screenshot will be saved in the current directory.

Format:

screenshot_YYYYMMDD_HHMMSS.png

---

# Brightness Control

Commands:

Increase brightness

Brightness up

Decrease brightness

Brightness down

---

# Volume Control

Commands:

Volume up

Increase volume

Volume down

Decrease volume

Mute

---

# Date and Time

Commands:

What time is it

What is today's date

---

# Web Search

Examples:

Search for Python tutorials

Search for machine learning

Open website github.com

Go to openai.com

---

# Local AI Chat (Ollama)

The assistant includes an integrated local LLM chat panel.

Current model:

mistral:7b-instruct-q5_K_M

Communication endpoint:

http://localhost:11434/api/chat

Features:

* Fully offline AI chat
* Streaming responses
* Text-to-speech output
* GUI chat interface

---

# Installation

## 1. Clone Project

```bash
git clone https://github.com/your-repository/Xeno.git

cd Xeno
```

## 2. Create Virtual Environment

Windows:

```bash
python -m venv venv

venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install tkinter
pip install SpeechRecognition
pip install pyttsx3
pip install requests
pip install psutil
pip install pyautogui
pip install screen-brightness-control
pip install pillow
pip install pyaudio
```

Optional:

```bash
pip install jupyterlab
```

---

# Ollama Setup

## Install Ollama

Windows/macOS/Linux:

https://ollama.com

Verify installation:

```bash
ollama --version
```

---

## Pull Mistral Model

```bash
ollama pull mistral:7b-instruct-q5_K_M
```

---

## Start Ollama Server

```bash
ollama serve
```

Server should be available at:

```text
http://localhost:11434
```

---

# Required Software

Recommended:

* Google Chrome
* Brave Browser
* VLC Media Player
* Visual Studio Code
* Jupyter Lab
* Ollama

---

# Voice Commands Reference

## Browser Commands

| Command     | Action               |
| ----------- | -------------------- |
| Open Chrome | Launch Chrome        |
| Open Brave  | Launch Brave         |
| New Tab     | Create new tab       |
| Close Tab   | Close current tab    |
| Refresh     | Refresh page         |
| History     | Open browser history |
| Downloads   | Open downloads       |

---

## System Commands

| Command           | Action                     |
| ----------------- | -------------------------- |
| Shutdown          | Shutdown PC                |
| Restart           | Restart PC                 |
| Sleep             | Put PC to sleep            |
| Lock Screen       | Lock workstation           |
| Open Task Manager | Launch task manager        |
| System Info       | Display system information |

---

## File Commands

| Command                | Action        |
| ---------------------- | ------------- |
| Create Folder Projects | Create folder |
| Create File notes.txt  | Create file   |
| Open Folder in VS Code | Open folder   |
| Open File in VS Code   | Open file     |

---

## Terminal Commands

| Command                   | Action              |
| ------------------------- | ------------------- |
| Open Terminal             | Launch terminal     |
| Run Command python app.py | Execute command     |
| Run Command git status    | Execute Git command |

---

# Running the Assistant

```bash
python Xeno.py
```

---

# Troubleshooting

## Microphone Not Detected

Install PyAudio:

```bash
pip install pyaudio
```

Windows users may need:

```bash
pip install pipwin

pipwin install pyaudio
```

---

## Ollama Connection Error

Check:

```bash
ollama serve
```

Verify:

```bash
curl http://localhost:11434
```

---

## VS Code Not Found

Add VS Code to system PATH.

Verify:

```bash
code --version
```

---

## Jupyter Not Found

Install:

```bash
pip install jupyterlab
```

Verify:

```bash
jupyter lab
```

---

# Project Architecture

```text
Xeno
│
├── Voice Recognition
├── Text To Speech
├── GUI Interface
├── Local LLM (Ollama)
├── System Automation
├── Browser Control
├── File Management
├── VS Code Integration
├── Jupyter Integration
├── Terminal Integration
├── Brightness Control
├── Screenshot Utility
└── System Monitoring
```

---

# Future Improvements

* Wake word detection ("Hey Xeno")
* Chat history memory
* Custom plugin system
* AI-powered desktop automation
* Smart home integration
* Face recognition login
* Email and calendar support
* Local document search (RAG)

---

# License

MIT License

Copyright (c) 2026

Feel free to modify and extend the project.
