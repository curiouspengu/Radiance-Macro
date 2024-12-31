from data.lib import config
import datetime

timers = []

# format of timers is as follows:
# [interval_time, last_run, function_to_run]

def add_timer(interval_time, function_to_run):
    global timers
    time = datetime.datetime.now() - datetime.timedelta(hours=5)
    timers.append([interval_time, time, function_to_run])

def initialize():
    global timers
    from data.potion_crafting import potion_crafting
    add_timer(int(config.config_data["potion_crafting"]["interval"]), potion_crafting.craft_potions)

def check_timers():
    global timers
    for timer in timers:
        duration = datetime.datetime.now() - timer[1]
        duration_in_s = duration.total_seconds()
        duration_in_m = divmod(duration_in_s, 60)[0]
        if duration_in_m > timer[0]:
            timer[1] = datetime.datetime.now()
            timer[2]()