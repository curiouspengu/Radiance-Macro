import ctypes
import multiprocessing
from time import sleep
import threading

try:
    from data.lib import config
except:
    ctypes.windll.user32.MessageBoxW(0, "Why the fuck are you running this file?\nWho told you to run this?", "Error", 0)
    exit(1)


from data.lib import window
from data.lib.auto import *
from data.lib import reconnect
from data.main_loop import timers

from data.lib import actionlib
from data.lib.actionlib import tap_ui_navigation

from pynput.keyboard import Key
import datetime

running = False
initialiazed = False
main_process = None

# treat this like a seperate file, everything gets reset
def main_loop():
    config.config_data = config.read_config()

    actionlib.load_actions()

    align_camera()
    timers.initialize()
    
    while True:
        timers.check_timers()
        sleep(10)


def inventory_screenshots():
    pass

def scan_for_slots():
    pass

def do_obby():
    pass

def check_counters():
    pass

def start():
    global main_process
    global running
    if running == True:
        ctypes.windll.user32.MessageBoxW(0, "Macro Already Running!", "Warning", 0)
        return
    else:
        running = True
        
    if window.focus_roblox() == -1:
        reconnect.do_reconnect()
    
    # reconnect_thread = threading.Thread(target=reconnect.check_reconnect, args=[[].append(main_process)])
    # reconnect_thread.start()

    main_process = multiprocessing.Process(target=main_loop)
    main_process.start()

def align_camera():
    exec(actionlib.get_action("align_camera.py"))

def stop():
    global running
    if running == True:
        running = False
    else:
        ctypes.windll.user32.MessageBoxW(0, "Macro Already Stopped", "Info", 0)
        return
    global main_process
    main_process.terminate()

def click_menu_button(button_num):
    exec(actionlib.get_action("click_menu_button.py"))

def align():
    pass