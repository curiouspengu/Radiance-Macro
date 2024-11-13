from ahk import AHK
from time import sleep
import ctypes
import win32gui
from data.lib import window

ahk = AHK()

def reset():
    ahk.key_press("esc")
    sleep(0.2)
    ahk.key_press("r")
    sleep(0.2)
    ahk.key_press("enter")

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