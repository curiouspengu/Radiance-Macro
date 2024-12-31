# TODO
from time import sleep

from data.lib import window
from data.lib import config

import win32gui

def check_reconnect(ref_main_process):
    if window.get_roblox_HWND() == -1:
        do_reconnect(ref_main_process)
    sleep(1)

def check_roblox_link():
    pass

def do_reconnect(ref_main_process = ""):
    if not ref_main_process == "":
        ref_main_process[0].terminate()
    sleep(1)
    # ahk.win_close(title=win32gui.GetWindowText(window.get_roblox_HWND()))
    # ahk.run_script(f"Run roblox://placeID=15532962292&linkCode={config.read_config("ps_link")}")

