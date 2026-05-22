import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import speech_recognition as sr
import pyttsx3
import threading
import time
import os
import webbrowser
import datetime
import requests
import json
import subprocess
import psutil
import pyautogui
import screen_brightness_control as sbc
from PIL import Image, ImageTk
import sys
import platform
import ctypes
import math

class AdvancedVoiceAssistant:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Voice Assistant - JARVIS System")
        self.root.geometry("1000x700")
        self.root.configure(bg='#0a0a0a')
        
        # Initialize speech engine
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 160)
        voices = self.engine.getProperty('voices')
        if len(voices) > 1:
            self.engine.setProperty('voice', voices[1].id)
        
        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Adjust for ambient noise
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
        
        self.is_listening = False
        self.current_app = None
        self.app_commands = {}
        self.system_status = {}
        
        # Application command mappings
        self.setup_app_commands()
        self.create_gui()
        self.update_system_status()
        
    def setup_app_commands(self):
        # Define commands for different applications
        self.app_commands = {
            'chrome': {
                'new tab': lambda: pyautogui.hotkey('ctrl', 't'),
                'close tab': lambda: pyautogui.hotkey('ctrl', 'w'),
                'next tab': lambda: pyautogui.hotkey('ctrl', 'tab'),
                'previous tab': lambda: pyautogui.hotkey('ctrl', 'shift', 'tab'),
                'refresh': lambda: pyautogui.hotkey('ctrl', 'r'),
                'bookmarks': lambda: pyautogui.hotkey('ctrl', 'shift', 'o'),
                'history': lambda: pyautogui.hotkey('ctrl', 'h'),
                'downloads': lambda: pyautogui.hotkey('ctrl', 'j'),
                'incognito': lambda: pyautogui.hotkey('ctrl', 'shift', 'n'),
                'find': lambda: pyautogui.hotkey('ctrl', 'f')
            },
            'notepad': {
                'save': lambda: pyautogui.hotkey('ctrl', 's'),
                'new file': lambda: pyautogui.hotkey('ctrl', 'n'),
                'open': lambda: pyautogui.hotkey('ctrl', 'o'),
                'select all': lambda: pyautogui.hotkey('ctrl', 'a'),
                'copy': lambda: pyautogui.hotkey('ctrl', 'c'),
                'paste': lambda: pyautogui.hotkey('ctrl', 'v'),
                'cut': lambda: pyautogui.hotkey('ctrl', 'x'),
                'undo': lambda: pyautogui.hotkey('ctrl', 'z'),
                'find': lambda: pyautogui.hotkey('ctrl', 'f'),
                'replace': lambda: pyautogui.hotkey('ctrl', 'h')
            },
            'file explorer': {
                'new folder': lambda: pyautogui.hotkey('ctrl', 'shift', 'n'),
                'rename': lambda: pyautogui.press('f2'),
                'copy': lambda: pyautogui.hotkey('ctrl', 'c'),
                'paste': lambda: pyautogui.hotkey('ctrl', 'v'),
                'delete': lambda: pyautogui.press('delete'),
                'select all': lambda: pyautogui.hotkey('ctrl', 'a'),
                'properties': lambda: pyautogui.hotkey('alt', 'enter'),
                'view large icons': lambda: pyautogui.hotkey('ctrl', 'shift', '2'),
                'view details': lambda: pyautogui.hotkey('ctrl', 'shift', '6')
            },
            'vlc': {
                'play': lambda: pyautogui.press('space'),
                'pause': lambda: pyautogui.press('space'),
                'stop': lambda: pyautogui.press('s'),
                'next': lambda: pyautogui.press('n'),
                'previous': lambda: pyautogui.press('p'),
                'volume up': lambda: pyautogui.press('ctrl', 'up'),
                'volume down': lambda: pyautogui.press('ctrl', 'down'),
                'fullscreen': lambda: pyautogui.press('f'),
                'mute': lambda: pyautogui.press('m')
            },
            'system': {
                'lock screen': self.lock_screen,
                'shutdown': self.shutdown_system,
                'restart': self.restart_system,
                'sleep': self.sleep_system,
                'task manager': self.open_task_manager,
                'system info': self.show_system_info
            }
        }
        
    def create_gui(self):
        # Header
        header_frame = tk.Frame(self.root, bg='#0a0a0a')
        header_frame.pack(fill=tk.X, padx=20, pady=10)
        
        title_label = tk.Label(
            header_frame, 
            text="JARVIS - Advanced Voice Assistant", 
            font=('Arial', 20, 'bold'),
            fg='#00ffcc',
            bg='#0a0a0a'
        )
        title_label.pack(side=tk.LEFT)
        
        # Status indicator
        self.status_var = tk.StringVar(value="Ready")
        status_label = tk.Label(
            header_frame,
            textvariable=self.status_var,
            font=('Arial', 12),
            fg='#ffff00',
            bg='#0a0a0a'
        )
        status_label.pack(side=tk.RIGHT)
        
        # Main content area
        main_frame = tk.Frame(self.root, bg='#0a0a0a')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Left panel - Controls and status
        left_panel = tk.Frame(main_frame, bg='#0a0a0a')
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
        
        # Assistant visualization
        viz_frame = tk.Frame(left_panel, bg='#1a1a1a', relief=tk.RAISED, bd=1)
        viz_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Create a simple visualization using canvas
        self.viz_canvas = tk.Canvas(viz_frame, width=200, height=150, bg='#1a1a1a', highlightthickness=0)
        self.viz_canvas.pack(pady=10)
        self.draw_voice_visualization(0)
        
        # Control buttons
        control_frame = tk.Frame(left_panel, bg='#0a0a0a')
        control_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.listen_btn = tk.Button(
            control_frame,
            text="🎤 Start Listening",
            command=self.toggle_listening,
            font=('Arial', 12, 'bold'),
            bg='#007acc',
            fg='white',
            width=20,
            height=2
        )
        self.listen_btn.pack(pady=5)
        
        # System status
        status_frame = tk.Frame(left_panel, bg='#1a1a1a', relief=tk.RAISED, bd=1)
        status_frame.pack(fill=tk.X, pady=(0, 20))
        
        status_title = tk.Label(
            status_frame,
            text="System Status",
            font=('Arial', 12, 'bold'),
            fg='#00ffcc',
            bg='#1a1a1a'
        )
        status_title.pack(pady=5)
        
        self.cpu_label = tk.Label(
            status_frame,
            text="CPU: --%",
            font=('Arial', 10),
            fg='white',
            bg='#1a1a1a'
        )
        self.cpu_label.pack(anchor=tk.W, padx=10)
        
        self.memory_label = tk.Label(
            status_frame,
            text="Memory: --%",
            font=('Arial', 10),
            fg='white',
            bg='#1a1a1a'
        )
        self.memory_label.pack(anchor=tk.W, padx=10)
        
        self.disk_label = tk.Label(
            status_frame,
            text="Disk: --%",
            font=('Arial', 10),
            fg='white',
            bg='#1a1a1a'
        )
        self.disk_label.pack(anchor=tk.W, padx=10)
        
        # Quick commands
        commands_frame = tk.Frame(left_panel, bg='#1a1a1a', relief=tk.RAISED, bd=1)
        commands_frame.pack(fill=tk.BOTH, expand=True)
        
        commands_title = tk.Label(
            commands_frame,
            text="Quick Commands",
            font=('Arial', 12, 'bold'),
            fg='#00ffcc',
            bg='#1a1a1a'
        )
        commands_title.pack(pady=5)
        
        # Create quick command buttons
        quick_commands = [
            ("Open Chrome", self.open_chrome),
            ("Open Notepad", self.open_notepad),
            ("Volume Up", self.volume_up),
            ("Volume Down", self.volume_down),
            ("Brightness +", self.brightness_up),
            ("Brightness -", self.brightness_down),
            ("Take Screenshot", self.take_screenshot),
            ("System Info", self.show_system_info)
        ]
        
        for cmd_text, cmd_func in quick_commands:
            btn = tk.Button(
                commands_frame,
                text=cmd_text,
                command=cmd_func,
                font=('Arial', 10),
                bg='#2a2a2a',
                fg='white',
                width=15
            )
            btn.pack(pady=2)
        
        # Right panel - Conversation and app controls
        right_panel = tk.Frame(main_frame, bg='#0a0a0a')
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Conversation log
        conv_frame = tk.Frame(right_panel, bg='#0a0a0a')
        conv_frame.pack(fill=tk.BOTH, expand=True)
        
        log_label = tk.Label(
            conv_frame,
            text="Conversation Log:",
            font=('Arial', 12, 'bold'),
            fg='white',
            bg='#0a0a0a'
        )
        log_label.pack(anchor=tk.W)
        
        self.conversation_log = scrolledtext.ScrolledText(
            conv_frame,
            wrap=tk.WORD,
            width=60,
            height=15,
            bg='#1a1a1a',
            fg='#00ffcc',
            font=('Consolas', 10),
            insertbackground='white'
        )
        self.conversation_log.pack(fill=tk.BOTH, expand=True, pady=5)
        self.conversation_log.config(state=tk.DISABLED)
        
        # Current app control frame
        self.app_control_frame = tk.Frame(right_panel, bg='#1a1a1a', relief=tk.RAISED, bd=1)
        self.app_control_frame.pack(fill=tk.X, pady=(10, 0))
        
        app_title = tk.Label(
            self.app_control_frame,
            text="Current Application: None",
            font=('Arial', 11, 'bold'),
            fg='#ff9900',
            bg='#1a1a1a'
        )
        app_title.pack(pady=5)
        
        self.app_commands_text = tk.Text(
            self.app_control_frame,
            wrap=tk.WORD,
            width=60,
            height=4,
            bg='#2a2a2a',
            fg='#cccccc',
            font=('Arial', 9),
            state=tk.DISABLED
        )
        self.app_commands_text.pack(fill=tk.X, padx=10, pady=5)
        
        # Start system monitoring
        self.monitor_system()
        
    def draw_voice_visualization(self, level):
        self.viz_canvas.delete("all")
        width = 200
        height = 150
        
        # Draw sound waves based on level
        center_x = width // 2
        center_y = height // 2
        
        for i in range(5):
            radius = 20 + i * 15 + level * 5
            color = f'#{min(255, 50 + i * 40 + level * 20):02x}{min(255, 200 + level * 10):02x}{min(255, 200 + i * 20):02x}'
            self.viz_canvas.create_oval(
                center_x - radius, center_y - radius,
                center_x + radius, center_y + radius,
                outline=color, width=2
            )
        
    def toggle_listening(self):
        if not self.is_listening:
            self.is_listening = True
            self.listen_btn.config(text="🔴 Stop Listening", bg='#cc0000')
            self.status_var.set("Listening...")
            self.add_to_log("System", "Voice recognition activated")
            self.listening_thread = threading.Thread(target=self.listen_loop)
            self.listening_thread.daemon = True
            self.listening_thread.start()
        else:
            self.is_listening = False
            self.listen_btn.config(text="🎤 Start Listening", bg='#007acc')
            self.status_var.set("Ready")
            self.add_to_log("System", "Voice recognition deactivated")
            self.draw_voice_visualization(0)
    
    def listen_loop(self):
        while self.is_listening:
            try:
                with self.microphone as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.2)
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                
                # Visual feedback
                for i in range(5):
                    if self.is_listening:
                        self.draw_voice_visualization(i)
                        time.sleep(0.1)
                
                command = self.recognizer.recognize_google(audio).lower()
                self.add_to_log("You", command)
                self.process_command(command)
                
            except sr.WaitTimeoutError:
                self.draw_voice_visualization(0)
            except sr.UnknownValueError:
                self.add_to_log("System", "Could not understand audio")
                self.draw_voice_visualization(0)
            except sr.RequestError as e:
                self.add_to_log("System", f"Speech recognition error: {e}")
                self.draw_voice_visualization(0)
            except Exception as e:
                self.add_to_log("System", f"Unexpected error: {e}")
                self.draw_voice_visualization(0)
    
    def process_command(self, command):
        response = ""
        
        # Application control commands
        if any(app in command for app in ['chrome', 'browser']):
            response = self.control_application('chrome', command)
        
        elif 'notepad' in command or 'text editor' in command:
            response = self.control_application('notepad', command)
        
        elif 'file explorer' in command or 'files' in command:
            response = self.control_application('file explorer', command)
        
        elif 'vlc' in command or 'media player' in command or 'video' in command:
            response = self.control_application('vlc', command)
        
        # System commands
        elif any(cmd in command for cmd in ['shutdown', 'restart', 'sleep', 'lock']):
            response = self.control_system(command)
        
        # Basic commands
        elif 'open chrome' in command:
            response = self.open_chrome()
        elif 'open notepad' in command:
            response = self.open_notepad()
        elif 'open calculator' in command:
            response = self.open_calculator()
        elif 'open file explorer' in command:
            response = self.open_file_explorer()
        elif 'open command prompt' in command:
            response = self.open_command_prompt()
        elif 'open task manager' in command:
            response = self.open_task_manager()
        
        # Media control
        elif any(cmd in command for cmd in ['volume up', 'increase volume']):
            response = self.volume_up()
        elif any(cmd in command for cmd in ['volume down', 'decrease volume']):
            response = self.volume_down()
        elif 'mute' in command:
            response = self.volume_mute()
        
        # Brightness control
        elif any(cmd in command for cmd in ['brightness up', 'increase brightness']):
            response = self.brightness_up()
        elif any(cmd in command for cmd in ['brightness down', 'decrease brightness']):
            response = self.brightness_down()
        
        # System info
        elif any(cmd in command for cmd in ['system info', 'system information']):
            response = self.show_system_info()
        
        # Screenshot
        elif 'screenshot' in command:
            response = self.take_screenshot()
        
        # Time and date
        elif 'time' in command:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            response = f"The current time is {current_time}"
        elif 'date' in command:
            current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
            response = f"Today's date is {current_date}"
        
        # Search commands
        elif 'search for' in command:
            query = command.replace('search for', '').strip()
            if query:
                webbrowser.open(f"https://www.google.com/search?q={query}")
                response = f"Searching for {query}"
            else:
                response = "What would you like me to search for?"
        
        # Website navigation
        elif 'open website' in command or 'go to' in command:
            site = command.replace('open website', '').replace('go to', '').strip()
            if site:
                if not site.startswith('http'):
                    site = 'https://' + site
                webbrowser.open(site)
                response = f"Opening {site}"
        
        # Application commands
        elif any(cmd in command for cmd in ['new tab', 'close tab', 'refresh', 'save', 'copy', 'paste']):
            response = self.execute_app_command(command)
        
        # Shutdown assistant
        elif any(cmd in command for cmd in ['shutdown', 'exit', 'quit', 'goodbye']):
            response = "Shutting down JARVIS. Goodbye!"
            self.add_to_log("Assistant", response)
            self.speak(response)
            self.root.after(1000, self.root.destroy)
            return
        
        else:
            response = "I'm not sure how to help with that. Try more specific commands."
        
        self.add_to_log("Assistant", response)
        self.speak(response)
    
    def control_application(self, app_name, command):
        # Open the application if not already open
        if f"open {app_name}" in command:
            if app_name == 'chrome':
                return self.open_chrome()
            elif app_name == 'notepad':
                return self.open_notepad()
            elif app_name == 'file explorer':
                return self.open_file_explorer()
            elif app_name == 'vlc':
                return self.open_vlc()
        
        # Set current application for context-aware commands
        self.current_app = app_name
        self.update_app_controls()
        
        return f"Ready to control {app_name}. You can now use application-specific commands."
    
    def execute_app_command(self, command):
        if not self.current_app:
            return "No application is currently active. Please open an application first."
        
        app_commands = self.app_commands.get(self.current_app, {})
        
        for cmd, action in app_commands.items():
            if cmd in command:
                try:
                    action()
                    return f"Executed {cmd} in {self.current_app}"
                except Exception as e:
                    return f"Error executing {cmd}: {str(e)}"
        
        return f"Command not recognized for {self.current_app}. Try different commands."
    
    def control_system(self, command):
        if 'shutdown' in command and 'computer' in command:
            return self.shutdown_system()
        elif 'restart' in command:
            return self.restart_system()
        elif 'sleep' in command:
            return self.sleep_system()
        elif 'lock' in command:
            return self.lock_screen()
        return "System command not recognized."
    
    # Application opening methods
    def open_chrome(self):
        try:
            webbrowser.open("https://www.google.com")
            self.current_app = 'chrome'
            self.update_app_controls()
            return "Opening Google Chrome"
        except Exception as e:
            return f"Error opening Chrome: {str(e)}"
    
    def open_notepad(self):
        try:
            os.system("notepad")
            self.current_app = 'notepad'
            self.update_app_controls()
            return "Opening Notepad"
        except Exception as e:
            return f"Error opening Notepad: {str(e)}"
    
    def open_calculator(self):
        try:
            if platform.system() == "Windows":
                os.system("calc")
            elif platform.system() == "Darwin":  # macOS
                os.system("open -a Calculator")
            else:  # Linux
                os.system("gnome-calculator")
            return "Opening Calculator"
        except Exception as e:
            return f"Error opening Calculator: {str(e)}"
    
    def open_file_explorer(self):
        try:
            if platform.system() == "Windows":
                os.system("explorer")
            elif platform.system() == "Darwin":
                os.system("open .")
            else:
                os.system("nautilus")
            self.current_app = 'file explorer'
            self.update_app_controls()
            return "Opening File Explorer"
        except Exception as e:
            return f"Error opening File Explorer: {str(e)}"
    
    def open_command_prompt(self):
        try:
            if platform.system() == "Windows":
                os.system("start cmd")
            elif platform.system() == "Darwin":
                os.system("open -a Terminal")
            else:
                os.system("gnome-terminal")
            return "Opening Command Prompt/Terminal"
        except Exception as e:
            return f"Error opening Command Prompt: {str(e)}"
    
    def open_task_manager(self):
        try:
            if platform.system() == "Windows":
                os.system("taskmgr")
            elif platform.system() == "Darwin":
                os.system("open -a 'Activity Monitor'")
            else:
                os.system("gnome-system-monitor")
            return "Opening Task Manager"
        except Exception as e:
            return f"Error opening Task Manager: {str(e)}"
    
    def open_vlc(self):
        try:
            if platform.system() == "Windows":
                os.system("vlc")
            elif platform.system() == "Darwin":
                os.system("open -a VLC")
            else:
                os.system("vlc")
            self.current_app = 'vlc'
            self.update_app_controls()
            return "Opening VLC Media Player"
        except Exception as e:
            return f"Error opening VLC: {str(e)}"
    
    # System control methods
    def shutdown_system(self):
        try:
            if platform.system() == "Windows":
                os.system("shutdown /s /t 5")
            elif platform.system() == "Darwin":
                os.system("sudo shutdown -h now")
            else:
                os.system("sudo shutdown -h now")
            return "System will shutdown in 5 seconds"
        except Exception as e:
            return f"Error shutting down: {str(e)}"
    
    def restart_system(self):
        try:
            if platform.system() == "Windows":
                os.system("shutdown /r /t 5")
            elif platform.system() == "Darwin":
                os.system("sudo shutdown -r now")
            else:
                os.system("sudo reboot")
            return "System will restart in 5 seconds"
        except Exception as e:
            return f"Error restarting: {str(e)}"
    
    def sleep_system(self):
        try:
            if platform.system() == "Windows":
                os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
            elif platform.system() == "Darwin":
                os.system("pmset sleepnow")
            else:
                os.system("systemctl suspend")
            return "Putting system to sleep"
        except Exception as e:
            return f"Error putting system to sleep: {str(e)}"
    
    def lock_screen(self):
        try:
            if platform.system() == "Windows":
                ctypes.windll.user32.LockWorkStation()
            elif platform.system() == "Darwin":
                os.system("pmset displaysleepnow")
            else:
                os.system("gnome-screensaver-command -l")
            return "Locking screen"
        except Exception as e:
            return f"Error locking screen: {str(e)}"
    
    # Media control methods
    def volume_up(self):
        try:
            pyautogui.press('volumeup')
            return "Volume increased"
        except Exception as e:
            return f"Error increasing volume: {str(e)}"
    
    def volume_down(self):
        try:
            pyautogui.press('volumedown')
            return "Volume decreased"
        except Exception as e:
            return f"Error decreasing volume: {str(e)}"
    
    def volume_mute(self):
        try:
            pyautogui.press('volumemute')
            return "Volume muted"
        except Exception as e:
            return f"Error muting volume: {str(e)}"
    
    # Brightness control
    def brightness_up(self):
        try:
            current = sbc.get_brightness()
            if isinstance(current, list):
                current = current[0]
            new = min(100, current + 10)
            sbc.set_brightness(new)
            return f"Brightness increased to {new}%"
        except Exception as e:
            return f"Error increasing brightness: {str(e)}"
    
    def brightness_down(self):
        try:
            current = sbc.get_brightness()
            if isinstance(current, list):
                current = current[0]
            new = max(0, current - 10)
            sbc.set_brightness(new)
            return f"Brightness decreased to {new}%"
        except Exception as e:
            return f"Error decreasing brightness: {str(e)}"
    
    # System information
    def show_system_info(self):
        try:
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # Memory usage
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            memory_total = round(memory.total / (1024**3), 2)
            memory_used = round(memory.used / (1024**3), 2)
            
            # Disk usage
            disk = psutil.disk_usage('/')
            disk_percent = disk.percent
            disk_total = round(disk.total / (1024**3), 2)
            disk_used = round(disk.used / (1024**3), 2)
            
            info = (f"System Information:\n"
                   f"CPU Usage: {cpu_percent}%\n"
                   f"Memory: {memory_used}GB / {memory_total}GB ({memory_percent}%)\n"
                   f"Disk: {disk_used}GB / {disk_total}GB ({disk_percent}%)\n"
                   f"OS: {platform.system()} {platform.release()}")
            
            return info
        except Exception as e:
            return f"Error getting system info: {str(e)}"
    
    def take_screenshot(self):
        try:
            screenshot = pyautogui.screenshot()
            filename = f"screenshot_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            screenshot.save(filename)
            return f"Screenshot saved as {filename}"
        except Exception as e:
            return f"Error taking screenshot: {str(e)}"
    
    def update_app_controls(self):
        # Update the app controls panel based on current app
        self.app_commands_text.config(state=tk.NORMAL)
        self.app_commands_text.delete(1.0, tk.END)
        
        if self.current_app:
            commands = self.app_commands.get(self.current_app, {})
            command_list = "\n".join([f"• {cmd}" for cmd in commands.keys()])
            self.app_commands_text.insert(tk.END, f"Available commands for {self.current_app}:\n{command_list}")
        else:
            self.app_commands_text.insert(tk.END, "No application active. Open an app to see available commands.")
        
        self.app_commands_text.config(state=tk.DISABLED)
    
    def update_system_status(self):
        try:
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=0.1)
            
            # Memory usage
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            
            # Disk usage
            disk = psutil.disk_usage('/')
            disk_percent = disk.percent
            
            self.cpu_label.config(text=f"CPU: {cpu_percent}%")
            self.memory_label.config(text=f"Memory: {memory_percent}%")
            self.disk_label.config(text=f"Disk: {disk_percent}%")
            
        except Exception as e:
            print(f"Error updating system status: {e}")
    
    def monitor_system(self):
        self.update_system_status()
        self.root.after(2000, self.monitor_system)  # Update every 2 seconds
    
    def speak(self, text):
        def speak_thread():
            self.engine.say(text)
            self.engine.runAndWait()
        
        threading.Thread(target=speak_thread, daemon=True).start()
    
    def add_to_log(self, speaker, text):
        self.conversation_log.config(state=tk.NORMAL)
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.conversation_log.insert(tk.END, f"[{timestamp}] {speaker}: {text}\n")
        self.conversation_log.see(tk.END)
        self.conversation_log.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = AdvancedVoiceAssistant(root)
    root.mainloop()