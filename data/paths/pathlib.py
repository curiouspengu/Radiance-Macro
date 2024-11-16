from ahk import AHK
from data.lib import config
from time import sleep

dev_walk_speed = 1.25 # VIP
azerty_replace_dict = {"w":"z", "a":"q"}

ahk = AHK()

def walk_time_conversion(d):
    final_walk_time = float(d) * (1.0 + (dev_walk_speed - 1.0) * (1.0 - float(config.read_config("vip_mode"))))
    return final_walk_time

def walk_sleep(d):
    sleep(walk_time_conversion(d))

def walk_send(k, t):
    if config.read_config("azerty_mode") == "1" and azerty_replace_dict[k]:
        k = azerty_replace_dict[k]
    
    result = lambda t: " " if not t == "" else ""
    ahk.send("{" + k + result(t) + t + "}")

def press(k, duration = 0.02):
    walk_send(k, "Down")
    sleep(duration)
    walk_send(k, "Up")

def jump():
    press("space")

def reset():
    ahk.press("esc")
    sleep(0.1)
    ahk.press("r")
    sleep(0.1)
    ahk.key_press("enter")
