from time import sleep
import subprocess
import ctypes

from lib import config
from lib.auto import *
from pynput.keyboard import Key

from PIL import ImageGrab
import requests

azerty_replace_dict = {"w":"z", "a":"q"}

ui_navigation_key = config.settings_data["ui_navigation_key"]

def walk_time_conversion(d):
    if config.settings_data["settings"]["vip+_mode"] == "1":
        return d
    elif config.settings_data["settings"]["vip_mode"] == "1":
        return d * 1.04
    else:
        return d * 1.3

def walk_sleep(d):
    sleep(walk_time_conversion(d))

def walk_send(k, t):
    if config.settings_data["settings"]["azerty_mode"] == "1" and azerty_replace_dict[k]:
        k = azerty_replace_dict[k]
    
    if t == True:
        kc.press(k)
    else:
        kc.release(k)

def tap_sleep(short=False):
    if short == True:
        sleep(float(config.settings_data["settings"]["sleep"]) / 2.0)
    else:
        sleep(float(config.settings_data["settings"]["sleep"]))

def tap_ui_navigation():
    kc.tap(ui_navigation_key)
    tap_sleep()

def reset():
    tap(Key.esc)
    tap("r")
    tap(Key.enter)

def tap(key):
    kc.tap(key)
    tap_sleep()

def get_action(file):
    with open(".p.txt", encoding="utf-8") as path_file:
        with open(f'{path_file.read()}\\data\\path_cache\\{file}', encoding="utf-8") as file:
            return file.read()

def load_actions():
    for action in config.settings_data["actions"]:
        with open(".p.txt", encoding="utf-8") as path_file:
            with open(f"{path_file.read()}\\data\\path_cache\\{action}.py", "w", encoding="utf-8") as file:
                link = config.settings_data["actions"][action]
                if "https://" in link:
                    file.write(requests.get(link).text)
                else:
                    try:
                        with open(link, encoding="utf-8"):
                            file.write(link.read())
                    except:
                        ctypes.windll.user32.MessageBoxW(0, "Custom Action FileNotFound!", "Error", 0)
                        return -1

def detect_pixel_color(bbox, rgb):
    px = ImageGrab.grab(bbox).load()
    for x in range(0, bbox[2] - bbox[0]):
        for y in range(0, bbox[3] - bbox[1]):
            if px[x, y] == rgb:
                return True
    return False