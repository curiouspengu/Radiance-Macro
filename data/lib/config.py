from customtkinter import *
from PIL import Image, ImageDraw
import requests
import ctypes
import json


ONLINE_CONFIG_URL = "https://raw.githubusercontent.com/curiouspengu/Radiance-Macro/refs/heads/main/data/settings/config.json"
config_path = ""

def get_current_version():
    return read_config()["version"]

def read_config(key=""):
    try:
        with open(config_path) as config_file:
            config_data = json.load(config_file)
            if len(config_data) == 0:
                ctypes.windll.user32.MessageBoxW(0, "CONFIG DATA NOT FOUND", "Error", 0)
                exit(1)
            if not key == "":
                return config_data[key]
            return config_data
    except:
        ctypes.windll.user32.MessageBoxW(0, "CONFIG DATA ERROR", "Error", 0)

def read_remote():
    try:
        online_config_data = requests.get(ONLINE_CONFIG_URL).json()
        if len(online_config_data) == 0:
            ctypes.windll.user32.MessageBoxW(0, "ONLINE CONFIG DATA NOT FOUND", "Error", 0)
            exit(1)
        return online_config_data
    except:
        ctypes.windll.user32.MessageBoxW(0, "ONLINE URL NOT FOUND. CANNOT RUN UPDATE CHECKER", "Error", 0)

def save_config(config_data):
    with open(config_path, 'w') as config_file:
        json.dump(config_data, config_file, indent=4)

def generate_tk_list():
    config_data = read_config()
    tk_var_list = {}
    for key in config_data:
        tk_var_list[key] = StringVar(value=config_data[key])
    return tk_var_list

def save_tk_list(tk_var_list):
    config_data = read_config()
    for key in tk_var_list:
        config_data[key] = tk_var_list[key].get()
    save_config(config_data)

def set_path(path):
    global config_path
    config_path = f"{path}/data/settings/config.json"

def parent_path():
    return read_config("parent_path")

def round_corners(im, rad):
    circle = Image.new('L', (rad * 2, rad * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, rad * 2 - 1, rad * 2 - 1), fill=255)
    alpha = Image.new('L', im.size, 255)
    w, h = im.size
    alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
    alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
    alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
    alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
    im.putalpha(alpha)
    return im

def theme_path():
    return read_config()["theme_path"]

def read_theme(key=""):
    with open(f"{parent_path()}{theme_path()}") as theme_file:
        theme_data = json.load(theme_file)
        if len(theme_data) == 0:
            ctypes.windll.user32.MessageBoxW(0, "THEME FILE NOT FOUND", "Error", 0)
            exit(1)
        if not key == "":
            return theme_data[key]
        return theme_data

def read_json(path, key=""):
    with open(f"{parent_path()}{path}") as file:
        data = json.load(file)
        if len(data) == 0:
            ctypes.windll.user32.MessageBoxW(0, "JSON FILE NOT FOUND", "Error", 0)
            exit(1)
        if not key == "":
            return data[key]
        return data

def save_theme_path(path):
    config_data = read_config()
    config_data["theme_path"] = path
    save_config(config_data)

def convert_to_ahk():
    pass