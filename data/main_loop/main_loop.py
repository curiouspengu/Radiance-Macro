import ctypes
import multiprocessing
from time import sleep
import sys
import threading
import os

try:
    from lib import config
except:
    ctypes.windll.user32.MessageBoxW(0, "Why the fuck are you running this file?\nWho told you to run this?", "Error", 0)
    exit(1)


from lib import window
from lib.auto import *
from lib import reconnect
from main_loop import timers

from lib import actionlib
from lib.actionlib import tap_ui_navigation

from pynput.keyboard import Key
import datetime
import keyboard

running = False
initialiazed = False
main_process = None

# treat this like a seperate file, everything gets reset
def main_loop():
    print("[MAINLOOP STARTED]")
    actionlib.load_actions()

    align_camera()
    timers.initialize()
    
    while True:
        timers.check_timers()
        sleep(10)


def inventory_screenshots():
    pass

def start_kill_keybind():
    keyboard.wait(config.settings_data["system_keybinds"]["stop"])
    os.system("C:\\Windows\\System32\\taskkill.exe /F /IM python.exe")

def start_keybinds():
    keyboard.add_hotkey(config.settings_data["system_keybinds"]["start"], main_loop)
    multiprocessing.Process(target=start_kill_keybind).start()

    print("[KEYBINDS STARTED]")
    keyboard.wait()

def scan_for_slots():
    pass

def do_obby():
    pass

def check_counters():
    pass

def align_camera():
    exec(actionlib.get_action("align_camera.py"))

def click_menu_button(button_num):
    exec(actionlib.get_action("click_menu_button.py"))

def align():
    pass