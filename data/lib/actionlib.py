from time import sleep
import subprocess
import ctypes

from data.lib import config
from data.lib.auto import *
from pynput.keyboard import Key

import requests

azerty_replace_dict = {"w":"z", "a":"q"}

ui_navigation_key = config.config_data["ui_navigation_key"]

def walk_time_conversion(d):
    if config.config_data["settings"]["vip+_mode"] == "1":
        return d
    elif config.config_data["settings"]["vip_mode"] == "1":
        return d * 1.25
    else:
        return d * 1.3

def walk_sleep(d):
    sleep(walk_time_conversion(d))

def walk_send(k, t):
    if config.config_data["settings"]["azerty_mode"] == "1" and azerty_replace_dict[k]:
        k = azerty_replace_dict[k]
    
    if t == True:
        kc.press(k)
    else:
        kc.release(k)

def tap_sleep(short=False):
    if short == True:
        sleep(float(config.config_data["settings"]["sleep"]) / 2.0)
    else:
        sleep(float(config.config_data["settings"]["sleep"]))

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

def load_actions():
    for action in config.config_data["actions"]:
        with open(f"path_cache/{action}.py", "w") as path_file:
            link = config.config_data["actions"][action]
            if "https://" in link:
                path_file.write(requests.get(link).text)
            else:
                try:
                    with open(link):
                        path_file.write(link.read())
                except:
                    ctypes.windll.user32.MessageBoxW(0, "Custom Action FileNotFound!", "Error", 0)
                    return -1
def get_action(file):
    with open("path.txt") as path_file:
        with open(f'{path_file.read()}/path_cache/{file}') as file:
            return file.read()