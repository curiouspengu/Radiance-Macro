import ctypes
import multiprocessing
try:
    from data.lib import config
except:
    ctypes.windll.user32.MessageBoxW(0, "Why the fuck are you running this file?\nWho told you to run this?", "Error", 0)
    exit(1)
from data.paths import pathlib
from data.lib import window
from data.lib import recconect
from ahk import AHK
from time import sleep

main_procress = None
running = False
initialiazed = False

ahk = AHK()

def main_loop():
    while True:
        # run + check
        if window.focus_roblox() == -1:
            # recconect
            pass
        pathlib.reset()

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
    global main_procress
    global running
    if running == True:
        return
    else:
        running = True
        
    if window.focus_roblox() == -1:
        print("NO ROBLOX")
    
    window.get_roblox_window_pos(x=[], y=[], w=[], h=[])
    align_camera()
    # main_procress = multiprocessing.Process(target=main_loop)
    # main_procress.start()

def align_camera():
    window.get_roblox_window_pos(x:=[], y:=[], w:=[], h:=[])
    pathlib.reset()
    click_menu_button(2)
    sleep(0.1)
    ahk.mouse_move(381 * (w[0]/1920), 129 * (h[0]/1080))
    ahk.click()
    

def stop():
    global running
    running = False
    global main_procress
    main_procress.terminate()

def click_menu_button(button_num):
    window.get_roblox_window_pos(rx:=[], ry:=[], w:=[], h:=[])
    menu_button_spacing = 54 * (h[0]/1080)
    menu_button_width = 64 * (w[0]/1920)

    start_x = 354 * (h[0]/1080)
    start_y = 11 * (w[0]/1920)

    ahk.mouse_move(x = start_y + (int(menu_button_width/2)), y = start_x + (menu_button_spacing * button_num))
    ahk.click()


def align():
    pass