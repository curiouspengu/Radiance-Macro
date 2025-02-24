import ctypes
import json

from PIL import Image, ImageDraw

import requests


with open(".p.txt", "r", encoding="utf-8") as file:
    settings_path = f"{file.read()}\\settings.json"

with open(".p.txt", "r", encoding="utf-8") as file:
    config_path = f"{file.read()}\\data\\settings\\config.json"

config_data = None
settings_data = None

def get_current_version():
    return read_config()["version"]

def read_config():
    # try:
    with open(config_path, encoding="utf-8") as config_file:
        config_data = config_file.read()
        config_data = json.loads(config_data)
        if len(config_data) == 0:
            ctypes.windll.user32.MessageBoxW(0, "CONFIG DATA NOT FOUND", "Error", 0)
            exit(1)
        return config_data
    # except:
    #     ctypes.windll.user32.MessageBoxW(0, "CONFIG DATA ERROR!", "Error", 0)

def read_settings():
    with open(settings_path, encoding="utf-8") as settings_file:
        settings_data = settings_file.read()
        settings_data = json.loads(settings_data)
        if len(settings_data) == 0:
            ctypes.windll.user32.MessageBoxW(0, "SETTINGS DATA NOT FOUND", "Error", 0)
            exit(1)
        return settings_data
    
def read_resolution():
    return read_json(read_settings()["resolution"]["current"])

def save_resolution(data):
    with open(".p.txt", "r", encoding="utf-8") as file:
        path = file.read()
    with open(path + config_data["resolutions"]["resolution"], 'w', encoding="utf-8") as file:
        json.dump(data, file, indent=4)

def save_config(config_data_p):
    global config_data
    with open(config_path, 'w', encoding="utf-8") as config_file:
        json.dump(config_data_p, config_file, indent=4)
    config_data = read_config()

def iterate_generate_list(json_object, var_list):
    for i in range(len(json_object)):
        if type(json_object[i]) == dict:
            var_list[i] = {}
            iterate_generate_dict(json_object[i], var_list[i])
        elif type(json_object[i]) == list:
            var_list[i] = []
            iterate_generate_list(json_object[i], var_list[i])
        else:
            var_list.append(StringVar(value=json_object[i]))

def iterate_generate_dict(json_object, var_list):
    for key in json_object:
        if type(json_object[key]) == dict:
            var_list[key] = {}
            iterate_generate_dict(json_object[key], var_list[key])
        elif type(json_object[key]) == list:
            var_list[key] = []
            iterate_generate_list(json_object[key], var_list[key])
        else:
            var_list[key] = StringVar(value=json_object[key])

def generate_tk_resolution_list():
    config_data = read_resolution()
    tk_var_list = {}
    iterate_generate_dict(config_data, tk_var_list)
    return tk_var_list

def iterate_save_dict(json_object, var_list):
    for key in json_object:
        if type(var_list[key]) == dict:
            iterate_save_dict(json_object[key], var_list[key])
        elif type(var_list[key]) == list:
            iterate_save_list(json_object[key], var_list[key])
        elif type(var_list[key]) == str:
            json_object[key] = var_list[key]
        else:
            json_object[key] = var_list[key].get()

def iterate_save_list(json_object, var_list):
    for i in range(len(var_list)):
        if type(var_list[i]) == dict:
            iterate_save_dict(json_object[i], var_list[i])
        elif type(var_list[i]) == list:
            iterate_save_list(json_object[i], var_list[i])
        else:
            json_object[i] = var_list[i].get()

def save_tk_list(tk_var_list):
    config_data = read_config()
    iterate_save_dict(config_data, tk_var_list)
    save_config(config_data)

def save_tk_resolution_list(tk_var_list):
    data = read_resolution()
    iterate_save_dict(data, tk_var_list)
    save_resolution(data)

def parent_path():
    with open(".p.txt", "r", encoding="utf-8") as file:
        return file.read()

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
    if "/" in config_data["paths"]["theme"]:
        return config_data["paths"]["theme"]
    else:
        return f"{parent_path()}{config_data['themes'][config_data['paths']['theme']]}"

def read_theme(key=""):
    with open(theme_path(), encoding="utf-8") as theme_file:
        theme_data = json.load(theme_file)
        if len(theme_data) == 0:
            ctypes.windll.user32.MessageBoxW(0, "THEME FILE NOT FOUND", "Error", 0)
            exit(1)
        if not key == "":
            return theme_data[key]
        return theme_data

def read_json(path, key=""):
    with open(f"{parent_path()}{path}", encoding="utf-8") as file:
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

tk_var_list = None

def generate_tk_list():
    global tk_var_list
    config_data = read_config()
    tk_var_list = {}
    iterate_generate_dict(config_data, tk_var_list)

config_data = read_config()
settings_data = read_settings()
