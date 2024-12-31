from data.lib import config

from tkinter import filedialog
from customtkinter import *

DEFAULT_FONT_BOLD = "Segoe UI Semibold"
main_window = None

window = None

class PotionSettingsWindow(CTkToplevel):
    def __init__(self):
        super().__init__()
        self.after(196, lambda: self.wm_iconbitmap(f"{config.parent_path()}/data/images/tray_radiant.ico"))

        self.grab_set()
        self.geometry("260x392")
        self.title(f"Automatic Potion Crafting Settings")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.tk_var_list = config.generate_tk_list()
        
        set_default_color_theme(config.theme_path())
        self.configure(fg_color=config.read_theme("CTk")["fg_color"])

        h1 = CTkFont(DEFAULT_FONT_BOLD, size=20, weight="bold")
        h2 = CTkFont(DEFAULT_FONT_BOLD, size=15, weight="bold")

        self.potion_settings_frame = CTkFrame(master=self)
        self.potion_settings_frame.grid(row=0, column=0, sticky="n", padx=10, pady=10)
        potion_settings_label = CTkLabel(master=self.potion_settings_frame, text="Potion Settings", font=h1).grid(row=0, pady=5, columnspan=2)
        crafting_interval_label = CTkLabel(master=self.potion_settings_frame, text="Crafting Interval (minutes): ").grid(row=1, column=0, padx=(5, 0))

        self.crafting_interval = CTkEntry(master=self.potion_settings_frame, width=80, validate='all', validatecommand=(self.register(lambda char: char.isdigit()), '%P'))
        self.crafting_interval.insert(0, config.config_data["potion_crafting"]["interval"])
        self.crafting_interval.bind(command=self.update_potion_crafting_interval, sequence="<Return>")
        self.crafting_interval.grid(row=1, column=1, padx=5)

        row_num = 2
        for potion in config.config_data["potion_crafting"]["options"]:
            checkbox = CTkCheckBox(master=self.potion_settings_frame, text=potion, variable=self.tk_var_list["potion_crafting"]["options"][potion]["enabled"], onvalue="1", offvalue="0").grid(row=row_num, column=0, padx=5, pady=5, stick="w", columnspan=2)
            row_num += 1
        
        # TEMPORARY
        self.geometry("260x426")
        CTkCheckBox(master=self.potion_settings_frame, text="TEMPORARY AUTO ADD SWITCHER", variable=self.tk_var_list["potion_crafting"]["temporary_auto_add"], onvalue="1", offvalue="0").grid(row=row_num, column=0, padx=5, pady=5, stick="w", columnspan=2)
    
    # def update_potion_options(self):
    #     for option in config.config_data["potion_options"]:
    #         CTkCheckBox(master=self.potion_settings_frame, )
    #         dropdown_menu.grid(row=self.row_num, padx=5, column=0)
    #         z

    # def insert_potion_option(self):
    #     dropdown_menu = CTkOptionMenu(master=self.potion_settings_frame, values=pass, command=optionmenu_callback)

    def update_potion_crafting_interval(self):
        config.save_tk_list(self.tk_var_list)
        config.config_data["potion_crafting_interval"] = self.crafting_interval.get()
        config.save_config(config.config_data)

    def focus_window(self, event):
        try:
            event.widget.focus_set()
        except:
            pass

    def on_close(self):
        config.save_tk_list(self.tk_var_list)
        self.bind_all("<Button-1>", func=self.focus_window)
        self.unbind("<Any-ButtonRelease>")
        self.grab_release()
        self.destroy()


def open_potions_settings(main_window_id):
    global window
    global main_window
    main_window = main_window_id
    if window == None or not window.winfo_exists():
        window = PotionSettingsWindow()

    