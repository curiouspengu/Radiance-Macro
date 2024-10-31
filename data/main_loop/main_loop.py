import ctypes
import multiprocessing
try:
    from data.lib import config
except:
    ctypes.windll.user32.MessageBoxW(0, "Why the fuck are you running this file?\nWho told you to run this?", "Error", 0)
    exit(1)

main_procress = None
running = False

def main_loop():
    print("running")

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
    print("started")
    main_procress = multiprocessing.Process(target=main_loop)
    main_procress.start()

def stop():
    print("stopping")
    running = False
    global main_procress
    main_procress.terminate()