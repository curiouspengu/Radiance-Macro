from tkinter import filedialog
import ctypes

from data.lib import config

from customtkinter import *
from PIL import ImageTk

DEFAULT_FONT_BOLD = "Segoe UI Semibold"
main_window = None

window = None

class ActionSettingsWindow(CTkToplevel):
    def __init__(self):
        super().__init__()
        self.after(196, lambda: self.wm_iconbitmap(f"{config.parent_path()}/data/images/tray_radiant.ico"))
        
        self.grab_set()
        self.geometry("1000x400")
        self.title(f"Actions Settings")
        # self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        
        set_default_color_theme(config.theme_path())
        self.configure(fg_color=config.read_theme("CTk")["fg_color"])

        h1 = CTkFont(DEFAULT_FONT_BOLD, size=20, weight="bold")
        h2 = CTkFont(DEFAULT_FONT_BOLD, size=15, weight="bold")

        actions_frame = CTkFrame(master=self)
        actions_frame.grid(row=0, column=0, sticky="n", padx=10, pady=10)
        action_label = CTkLabel(master=actions_frame, text="Actions Settings", font=h1).grid(row=0, pady=5, columnspan=3)

        row_num = 1
        self.path_labels = {}
        for action in config.config_data["actions"]:
            action_label = CTkLabel(master=actions_frame, text=action.replace("_", " ").capitalize(), font=h2).grid(row=row_num, columnspan=3)
            row_num += 1
            self.path_labels[action] = CTkLabel(master=actions_frame, text=f'{config.config_data["actions"][action]}')
            self.path_labels[action].grid(row=row_num, padx=5, column=0)
            
            self.change_action_button = CTkButton(master=actions_frame, text=f'Change Action', command=lambda: self.change_action(action))
            self.change_action_button.grid(row=row_num, column=1, pady=(0, 5), sticky="w", padx=(0, 5))
            self.reset_action_button = CTkButton(master=actions_frame, text=f'Reset Action', command=lambda: self.reset_action(action))
            self.reset_action_button.grid(row=row_num, column=2, pady=(0, 5), sticky="w", padx=(0, 5))
            row_num += 1
    
    def reset_action(self, action):
        default_action_path = config.config_data["default_actions"][action]
        self.path_labels[action].configure(text=default_action_path)
        config.config_data["actions"][action] = default_action_path
        config.save_config(config.config_data)

    def change_action(self, action):
        self.iconify()
        main_window.iconify()
        filepath = filedialog.askopenfilename(initialdir = "/",
            title = "Select an action",
            filetypes = [("Python Files", "*.py*")]
        )
        main_window.deiconify()
        self.deiconify()
        self.path_labels[action].configure(text=filepath)
        config.config_data["actions"][action] = filepath
        config.save_config(config.config_data)


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


def open_actions_settings(main_window_id):
    global window
    global main_window
    main_window = main_window_id
    if ctypes.windll.user32.MessageBoxW(0, "This menu is for developers and advanced users only as it contains code that may break your macro!\nDo you wish to continue?", "Warning", 4) == 7:
        return
    if window == None or not window.winfo_exists():
        window = ActionSettingsWindow()

    