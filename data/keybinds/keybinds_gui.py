from data.lib import config
from data.main_gui import main_gui

from customtkinter import *
from pynput import keyboard
from PIL import ImageTk

DEFAULT_FONT_BOLD = "Segoe UI Semibold"
main_window = None

keybind = ""
global_parent_config = ""
global_config_key = ""
window = None
count = 0

class KeybindsWindow(CTkToplevel):
    def __init__(self, feature):
        super().__init__()
        self.after(196, lambda: self.wm_iconbitmap(f"{config.parent_path()}/data/images/tray_radiant.ico"))
        
        self.grab_set()
        self.geometry("350x150")
        self.title(f"{feature} Keybinds")
        # self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.configure(fg_color=config.read_theme("CTkFrame")["fg_color"])

        set_default_color_theme(f'{config.config_data["paths"]["parent_path"]}{config.theme_path()}')

        self.iconpath = ImageTk.PhotoImage(file=f"{config.parent_path()}/data/images/tray_radiant.png")
        self.wm_iconbitmap()
        self.iconphoto(False, self.iconpath)

        h1 = CTkFont(DEFAULT_FONT_BOLD, size=20, weight="bold")

        keybind_frame = CTkFrame(master=self)
        keybind_frame.place(relx=.5, rely=.5, anchor="center")

        self.keybind_label = CTkLabel(master=keybind_frame, text=f"Enter Keybind", font=h1)
        self.keybind_label.grid(row=0, columnspan=2, pady=(0, 10))
        clear_button = CTkButton(master=keybind_frame, text="Clear", command=self.clear_keybind).grid(row=1, column=0, padx=5, pady=5)
        save_button = CTkButton(master=keybind_frame, text="Save", command=save_keybinds).grid(row=1, column=1, padx=5, pady=5)
        
        listener = keyboard.Listener(
            on_press=self.append)
        listener.start()
        

    def focus_window(self, event):
        try:
            event.widget.focus_set()
        except:
            pass

    def on_close(self):
        self.bind_all("<Button-1>", func=self.focus_window)
        self.unbind("<Any-ButtonRelease>")
        self.grab_release()
        self.destroy()
    
    def clear_keybind(self):
        global count
        global keybind
        count = 0
        keybind = ""
        self.keybind_label.configure(text="Enter Keybind")
    
    def append(self, key):
        global count
        global keybind

        try:
            keypress_event = key.char
        except AttributeError:
            keypress_event = key
        keypress_event = str(keypress_event).replace("Key.", "")
    
        if not keypress_event in keybind.split("+"):
            if count > 4:
                return
            else:
                count += 1
            
            if not keybind == "":
                keybind += "+"
            keybind += str(keypress_event)
        try:
            self.keybind_label.configure(text=keybind.upper())
        except:
            pass

def save_keybinds():
    if keybind == "\\":
        global_parent_config[global_config_key] = "\\"    
    global_parent_config[global_config_key] = keybind
    config.save_config(config.config_data)
    main_gui.MainWindow.reload_config_data(main_window)
    window.on_close()

def get_keybinds(main_window_id, feature, parent_config, config_key):
    global global_parent_config
    global global_config_key
    global window
    global main_window
    global keybind
    keybind = ""
    main_window = main_window_id

    global_parent_config = parent_config
    global_config_key = config_key
    if window == None or not window.winfo_exists():
        window = KeybindsWindow(feature)

    
 