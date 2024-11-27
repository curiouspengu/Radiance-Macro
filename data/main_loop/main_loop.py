import ctypes
import multiprocessing
try:
    from data.lib import config
except:
    ctypes.windll.user32.MessageBoxW(0, "Why the fuck are you running this file?\nWho told you to run this?", "Error", 0)
    exit(1)
from data.paths import pathlib
from data.lib import window
from data.lib.ahk import ahk
from data.lib import reconnect
from time import sleep
from tkinter import messagebox
import threading

running = False
initialiazed = False
main_process = None

def main_loop(config_path):
    config.set_path(config_path)
    while True:
        # run + check
        # print("running")
        pathlib.reset()
        sleep(10)


def inventory_screenshots():
    pass

def scan_for_slots():
    pass

def align_camera():
    pass

def do_obby():
    pass

def check_counters():
    pass

def start():
    global main_process
    global running
    if running == True:
        messagebox.showwarning(title="Warning", message="Macro Already Running!")
        return
    else:
        running = True
        
    if window.focus_roblox() == -1:
        print("NO ROBLOX")
        reconnect.do_reconnect()
    
    align_camera()
    reconnect_thread = threading.Thread(target=reconnect.check_reconnect, args=[[].append(main_process)])
    reconnect_thread.start()
    main_process = multiprocessing.Process(target=main_loop, args=[config.read_config("parent_path")])
    main_process.start()

def align_camera():
    pathlib.reset()
    click_menu_button(2)
    sleep(0.1)
    r_pos = window.get_roblox_window_pos()
    ahk.mouse_move(381 * (r_pos.width/1920.0), 143 * (r_pos.height/1080.0))
    
    ahk.click()
    sleep(0.1)
    ahk.mouse_drag(button="R", from_position=[r_pos.x + r_pos.width*0.2, r_pos.y + 44 + r_pos.height*0.05], x=r_pos.x + r_pos.width*0.2, y=r_pos.y + 400 + r_pos.height*0.05, send_mode="Input", speed=1)
    sleep(0.1)
    for i in range(50):
        ahk.click(button="WU")
        sleep(0.01)
    for i in range(15):
        ahk.click(button="WD")
        sleep(0.01)


def stop():
    global running
    if running == True:
        running = False
    else:
        messagebox.showwarning(title="Warning", message="Macro Already Stopped!")
        return
    global main_process
    main_process.terminate()

def click_menu_button(button_num):
    rel_pos = window.get_roblox_window_pos()
    menu_button_spacing = 54 * (rel_pos.height/1080)
    menu_button_width = 64 * (rel_pos.width/1920)

    start_y = 367 * (rel_pos.height/1080)
    start_x = 11 * (rel_pos.width/1920)

    ahk.mouse_move(x = start_x + (int(menu_button_width/2)), y = start_y + (menu_button_spacing * button_num))
    ahk.click()
    


def align():
    pass