from customtkinter import *
from data.lib import config
from data.main_gui import main_gui

DEFAULT_FONT_BOLD = "Segoe UI Semibold"
readable_keybinds = config.read_json("/data/keybinds/readable_keybinds.json")
ahk_keybind_dict = config.read_json("/data/lib/ahk_keybinds_dict.json")
main_window = None

keybind = ""
global_config_key = ""
window = None
count = 0

class KeybindsWindow(CTkToplevel):
    def __init__(self, feature):
        super().__init__()
        
        self.grab_set()
        self.geometry("350x150")
        self.title(f"{feature} Keybinds")
        # self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.configure(fg_color=config.read_theme("CTkFrame")["fg_color"])

        h1 = CTkFont(DEFAULT_FONT_BOLD, size=20, weight="bold")

        keybind_frame = CTkFrame(master=self)
        keybind_frame.place(relx=.5, rely=.5, anchor="center")

        self.keybind_label = CTkLabel(master=keybind_frame, text=f"Enter Keybind", font=h1)
        self.keybind_label.grid(row=0, columnspan=2, pady=(0, 10))
        clear_button = CTkButton(master=keybind_frame, text="Clear", command=self.clear_keybind).grid(row=1, column=0, padx=5, pady=5)
        save_button = CTkButton(master=keybind_frame, text="Save", command=save_keybinds).grid(row=1, column=1, padx=5, pady=5)
        
        self.bind("<KeyPress>", self.append)

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
    
    def append(self, keypress):
        global count
        global keybind
        global readable_keybinds
        global ahk_keybind_dict

        keypress_event = keypress.keysym
    
        if not keypress_event in keybind.split(" + "):
            if count > 4:
                return
            else:
                count += 1
            
            if not keybind == "":
                keybind += " + "
            keybind += keypress_event
        self.keybind_label.configure(text=keybind.upper())
        

def save_keybinds():
    config_data = config.read_config()
    config_data[global_config_key] = keybind
    config.save_config(config_data)
    main_gui.MainWindow.reload_config_data(main_window)
    window.on_close()

def get_keybinds(main_window_id, feature, config_key):
    global global_config_key
    global window
    global main_window
    global keybind
    keybind = ""
    main_window = main_window_id

    global_config_key = config_key
    if window == None or not window.winfo_exists():
        window = KeybindsWindow(feature)

    
 