import win32gui

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

def get_roblox_window_pos(x: list,y: list,w: list,h: list, hwnd=None):
    # Passing by reference
    if not hwnd:
        hwnd = get_roblox_HWND()
    if hwnd == -1:
        return -1
    rect = win32gui.GetWindowRect(hwnd)
    x.append(rect[0])
    y.append(rect[1])
    w.append(rect[2] - x[0])
    h.append(rect[3] - y[0])