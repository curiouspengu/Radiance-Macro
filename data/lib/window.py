import win32gui
from data.lib.ahk import ahk
def windowEnumerationHandler(hwnd, top_windows):
    top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))

def get_roblox_HWND():
    top_windows = []
    win32gui.EnumWindows(windowEnumerationHandler, top_windows)
    for i in top_windows:
        if "roblox" in i[1].lower():
            return i[0]
    return -1

def focus_roblox():
    roblox_hwnd = get_roblox_HWND()
    if roblox_hwnd == -1:
        return -1
    win32gui.ShowWindow(roblox_hwnd, 5)
    win32gui.SetForegroundWindow(roblox_hwnd)

class Position():
    def __init__(self):
        super().__init__()
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0


def get_roblox_window_pos():
    position = ahk.win_get_position(title=win32gui.GetWindowText(get_roblox_HWND()))
    if position.x == -8 and position.y == -8:
        position1 = Position()
        position1.x = 0
        position1.y = 23
        position1.width = position.width - 16
        position1.height = position.height - 24
        print(position.x)
        print(position.y)
        print(position.width)
        print(position.height)
        print()
        print(position1.x)
        print(position1.y)
        print(position1.width)
        print(position1.height)
        return position1
    return position