import ctypes
from time import sleep

try:
    from lib import config
except ImportError:
    ctypes.windll.user32.MessageBoxW(0, "CONFIG FILE NOT FOUND", "Error", 0)

from lib.auto import kc, ahk
from lib.actionlib import *
from lib import window

from PIL import ImageGrab
from pynput.keyboard import Key

def craft_potion(potion_name):
    exec(get_action("craft_potion.py"))

    # TEMPORARY Auto Add
    if potion_name == config.config_data["potion_crafting"]["current_temporary_auto_add"]:
        tap_ui_navigation()
        tap(Key.left)
        tap(Key.left)
        tap(Key.down)
        tap(Key.up)
        tap(Key.enter)
        tap_ui_navigation()

def craft_potions():
    # TEMPORARY AUTO ADD
    
    first = False
    if config.settings_data["potion_crafting"]["temporary_auto_add"] == "1":
        for _ in range(2):
            for potion in config.config_data["potion_crafting"]["options"]:
                if config.settings_data["potion_crafting"]["options"][potion] == "1":
                    if potion == config.config_data["potion_crafting"]["current_temporary_auto_add"]:
                        first = True
                    elif first == True:
                        config.config_data["potion_crafting"]["current_temporary_auto_add"] = potion
                        config.save_config(config.config_data)
                        break
            if first == False:
                for potion in config.config_data["potion_crafting"]["options"]:
                    if config.settings_data["potion_crafting"]["options"][potion] == "1":
                        config.config_data["potion_crafting"]["current_temporary_auto_add"] = potion
                        config.save_config(config.config_data)
                        break            
    # ACUTAL PROGRAM
    exec(get_action("potion_path.py"))
    for potion in config.config_data["potion_crafting"]["options"]:
        if config.settings_data["potion_crafting"]["options"][potion] == "1":
            craft_potion(potion)
    
    # Close and End
    tap_ui_navigation()
    tap(Key.left)
    tap(Key.enter)
    tap_ui_navigation()
    reset()