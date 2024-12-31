import ctypes
from time import sleep
import threading
from tkinter import filedialog

try:
    from data.lib import config
except:
    ctypes.windll.user32.MessageBoxW(0, "Why the fuck are you running this file?\nWho told you to run this?", "Error", 0)
    exit(1)

from data.keybinds import keybinds_gui
from data.main_loop import main_loop
from data.lib.auto import ahk
from data.lib import actions_settings_gui
from data.potion_crafting import potion_crafting_gui

import keyboard
from pynput.keyboard import Key

from customtkinter import *
from PIL import ImageTk, Image

deactivate_automatic_dpi_awareness()

CURRENT_VERSION = config.get_current_version()
DEFAULT_FONT = "Segoe UI"
DEFAULT_FONT_BOLD = "Segoe UI Semibold"
MAX_WIDTH = 1000

class MainWindow(CTk):
    def __init__(self):
        super().__init__()
        self.bind_all("<Button-1>", self.focus_widget)
        self.title(f"Radiance Macro v{CURRENT_VERSION}")
        self.geometry("630x315x200x200")
        self.resizable(False, False)
        self.grid_columnconfigure(0, weight=1)
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.iconpath = ImageTk.PhotoImage(file=f"{config.parent_path()}/data/images/tray_radiant.png")
        self.wm_iconbitmap()
        self.iconphoto(True, self.iconpath)
        
        self.aura_recording_keybind_window = None
        self.tk_var_list = config.generate_tk_list()

        set_default_color_theme(config.theme_path())
        self.configure(fg_color=config.read_theme("CTk")["fg_color"])

        self.tab_control = CTkTabview(master=self, height=265, fg_color=config.read_theme("CTkTabview")["fg_color"])
        
        main_tab = self.tab_control.add("Main")
        crafting_tab = self.tab_control.add("Crafting")
        discord_tab = self.tab_control.add("Discord")
        merchant_tab = self.tab_control.add("Merchant")
        settings_tab = self.tab_control.add("Settings")
        extras_tab = self.tab_control.add("Extras")
        credits_tab = self.tab_control.add("Credits")

        self.tab_control.set("Credits")
        self.tab_control.grid(padx=10)

        for button in self.tab_control._segmented_button._buttons_dict.values():
            button.configure(width=MAX_WIDTH, height=35, corner_radius=10, font=CTkFont(DEFAULT_FONT_BOLD, size=15, weight="bold"))
        
    
        system_button_frame = CTkFrame(master=self)
        system_button_frame.grid(row=1, pady=(5, 8), padx=6, sticky="s")

        self.start_button = CTkButton(master=system_button_frame, text=f'Start ({config.config_data["system_keybinds"]["start"]})', command=self.start, height=30, width=100, corner_radius=4)
        self.start_button.grid(row=0, column=0, padx=4, pady=4)
        
        self.stop_button = CTkButton(master=system_button_frame, text=f'Stop ({config.config_data["system_keybinds"]["stop"]})', command=self.stop, height=30, width=100, corner_radius=4)
        self.stop_button.grid(row=0, column=2, padx=4, pady=4)

        keyboard.add_hotkey(config.config_data["system_keybinds"]["start"], self.start)
        keyboard.add_hotkey(config.config_data["system_keybinds"]["stop"], self.stop)
        keyboard.add_hotkey("f3", self.restart)

        # FONTS
        h1 = CTkFont(DEFAULT_FONT_BOLD, size=20, weight="bold")
        h2 = CTkFont(DEFAULT_FONT_BOLD, size=15, weight="bold")

        text = CTkFont(DEFAULT_FONT, size=12, weight="normal")

        obby_frame = CTkFrame(master=main_tab)
        obby_frame.grid(row=0, column=0, sticky="n", padx=(1, 1))
        obby_title_label = CTkLabel(master=obby_frame, text="Obby", font=h1).grid(row=0, column=1)
        do_obby_checkbox = CTkCheckBox(state="disabled", master=obby_frame, text="Do Obby (30% Luck Boost Every 2 Mins)", variable=self.tk_var_list["obby"]["enabled"], onvalue="1", offvalue="0").grid(row=2, column=1, padx=5, pady=5, stick="w")
        check_for_obby_buff_check_box = CTkCheckBox(state="disabled", master=obby_frame, text="Check for Obby Buff Effect", variable=self.tk_var_list["obby"]["check_for_buff"], onvalue="1", offvalue="0").grid(row=3, column=1, padx=5, pady=5, stick="w")

        auto_equip_frame = CTkFrame(master=main_tab, width=200, height=31)
        auto_equip_frame.grid(row=0, column=1, stick="n", padx=(5, 0))
        auto_equip_title = CTkLabel(master=auto_equip_frame, text="Auto Equip", font=h1).grid(row=0, pady=(0, 3), columnspan=2)

        enable_auto_equip = CTkCheckBox(state="disabled", master=auto_equip_frame, text="Enable Auto Equip", variable=self.tk_var_list["auto_equip"]["enabled"], onvalue="1", offvalue="0").grid(row=1, pady=(1, 6), sticky="w", padx=(5, 4))
        self.auto_equip_aura = CTkEntry(state="disabled", master=auto_equip_frame, placeholder_text="Aura", width=330)
        self.auto_equip_aura.bind(command=self.update_auto_equip_aura, sequence="<Return>")
        if not config.config_data["auto_equip"]["aura"] == "":
            self.auto_equip_aura.insert(0, config.config_data["auto_equip"]["aura"])
            
        
        self.auto_equip_aura.grid(row=2, column=0, padx=5, sticky="e", pady=(0, 6))

        paths_frame = CTkFrame(master=main_tab)
        paths_frame.grid(row=1, pady=(6, 0), column=0, padx=(1, 0))
        
        paths_title = CTkLabel(master=paths_frame, text="Paths", font=h1, width=240).grid(row=0, padx=5)

        enable_collect_items = CTkCheckBox(state="disabled", master=paths_frame, text="Enable Item Collection", variable=self.tk_var_list["collect_items"], onvalue="1", offvalue="0").grid(row=1, sticky="w", padx=5, pady=5)
        autograil = CTkCheckBox(state="disabled", master=paths_frame, text="Auto grail", variable=self.tk_var_list["auto_grail"]["enabled"], onvalue="1", offvalue="0").grid(row=2, sticky="w", padx=5, pady=5)

        reconnect_frame = CTkFrame(master=main_tab, width=200, height=31)
        reconnect_frame.grid(row=1, column=1, stick="n", padx=(5, 0), pady=(6, 0))
        reconnect_title = CTkLabel(master=reconnect_frame, text="Auto reconnect", font=h1).grid(row=0, pady=(0, 3))
    
        enable_reconnect = CTkCheckBox(state="disabled", master=reconnect_frame, text="Enable Auto reconnect", variable=self.tk_var_list["auto_reconnect"]["enabled"], onvalue="1", offvalue="0").grid(row=1, pady=(1, 6), sticky="w", padx=(5, 4))
        self.ps_link = CTkEntry(state="disabled", master=reconnect_frame, placeholder_text="Private Server Link", width=330)
        self.ps_link.bind(command=self.update_auto_reconnect_ps_link, sequence="<Return>")
        if not config.config_data["ps_link"] == "":
            self.ps_link.insert(0, config.config_data["ps_link"])
        self.ps_link.grid(row=2, column=0, padx=5, sticky="e", pady=(0, 6))

        item_crafting_frame = CTkFrame(master=crafting_tab)
        item_crafting_frame.grid(row=0, column=0, padx=(1, 0))
        item_crafting_title = CTkLabel(master=item_crafting_frame, text="Automatic Item Crafting", font=h1).grid(row=0, padx=5)
        enable_item_crafting_checkbox = CTkCheckBox(state="disabled", master=item_crafting_frame, text="Enable Automatic Item Crafting", variable=self.tk_var_list["item_crafting"]["enabled"], onvalue='1', offvalue='0').grid(row=1, padx=5, pady=5, sticky="w")
        item_crafting_settings_button = CTkButton(state="disabled", master=item_crafting_frame, text="Automatic Item Crafting Settings", command=self.open_automatic_item_crafting_settings, width=286).grid(padx=5, pady=5)

        potion_crafting_frame = CTkFrame(master=crafting_tab)
        potion_crafting_frame.grid(row=0, column=1, padx=(6, 5), sticky="n")
        potion_crafting_title = CTkLabel(master=potion_crafting_frame, text="Automatic Potion Crafting", font=h1).grid(row=0, padx=5)
        enable_potion_crafting_checkbox = CTkCheckBox(master=potion_crafting_frame, text="Enable Automatic Potion Crafting", variable=self.tk_var_list["potion_crafting"]["enabled"], onvalue='1', offvalue='0').grid(row=1, padx=5, pady=5, sticky="w")
        potion_crafting_settings_button = CTkButton(master=potion_crafting_frame, text="Automatic Potion Crafting Settings", width=284, command=lambda: potion_crafting_gui.open_potions_settings(self)).grid(row=2, padx=5, pady=5)

        cycle_auto_add_settings_frame = CTkFrame(master=crafting_tab)
        cycle_auto_add_settings_frame.grid(row=1, columnspan=2, sticky="w", pady=(6, 0), padx=(1, 0))
        switch_auto_add_title = CTkLabel(master=cycle_auto_add_settings_frame, text='Cycle "Auto Add"', font=h1).grid(row=0)
        enable_switch_auto_add_checkbox = CTkCheckBox(state="disabled", master=cycle_auto_add_settings_frame, text='Enable Cycle "Auto Add" (For both Potion Crafting and Item Crafting)', variable=self.tk_var_list["cycle_auto_add"]["enabled"], onvalue="1", offvalue="0").grid(row=1, padx=5, sticky="w", pady=5)
        cycle_auto_add_settings = CTkButton(state="disabled", master=cycle_auto_add_settings_frame, text="Cycle Auto Add Settings", width=586).grid(row=2, padx=5, pady=5)

        discord_webhook_frame = CTkFrame(master=discord_tab)
        discord_webhook_frame.grid(row=0, column=0, sticky="n", pady=(0, 0), padx=(1, 0))
        discord_webhook_title = CTkLabel(master=discord_webhook_frame, text="Discord Webhooks", font=h1).grid(row=0, padx=5)
        enable_discord_webhook = CTkCheckBox(state="disabled", master=discord_webhook_frame, text="Enable Discord Webhooks", variable=self.tk_var_list['discord']["webhook"]["enabled"], onvalue="1", offvalue="0").grid(row=1, padx=5, pady=5, sticky="w")
        discord_webhook_list = CTkButton(state="disabled", master=discord_webhook_frame, text="Add Discord Webhook", command=self.open_add_discord_webhook, width=286).grid(row=2, padx=5, pady=5)
        discord_webhook_settings = CTkButton(state="disabled", master=discord_webhook_frame, text="Discord Webhook Settings", command=self.open_discord_webhook_settings, width=286).grid(row=3, padx=5, pady=5)
        
        discord_bot_frame = CTkFrame(master=discord_tab)
        discord_bot_frame.grid(row=0, column=1, sticky="n", pady=(0, 0), padx=(6, 0))
        discord_bot_title = CTkLabel(master=discord_bot_frame, text="Discord Bot", font=h1).grid(row=0, padx=5)
        enable_discord_bot = CTkCheckBox(state="disabled", master=discord_bot_frame, text="Enable Discord Bot", variable=self.tk_var_list["discord"]["bot"]["enabled"], onvalue="1", offvalue="0").grid(row=1, padx=5, pady=5, sticky="w")
        add_discord_bot_button = CTkButton(state="disabled", master=discord_bot_frame, text="Add Discord Bot", command=self.open_add_discord_bot, width=285).grid(row=2, padx=5, pady=5)
        discord_bot_settings_button = CTkButton(state="disabled", master=discord_bot_frame, text="Discord Bot Settings", command=self.open_discord_bot_settings, width=285).grid(row=3, padx=5, pady=5)

        community_frame = CTkFrame(master=discord_tab)
        community_frame.grid(row=1, columnspan=2, pady=(6, 0), padx=(1, 0), sticky="n")
        community_title = CTkLabel(master=community_frame, text="Community", font=h1, width=586).grid(row=0, padx=5)
        coming_soon = CTkLabel(master=community_frame, text="Website Coming Soon", width=586).grid(row=1, padx=5, pady=(3, 3))

        jester_frame = CTkFrame(master=merchant_tab)
        jester_frame.grid(row=0, column=0, sticky="n", padx=(1, 0))
        jester_title = CTkLabel(master=jester_frame, text="Jester Autobuy", font=h1).grid(row=0, padx=5)
        enable_jester_autobuy = CTkCheckBox(state="disabled", master=jester_frame, text="Enable Jester Autobuy", variable=self.tk_var_list['jester_autobuy'], onvalue="1", offvalue="0").grid(row=1, pady=5, padx=5, sticky="w")
        jester_item_settings = CTkButton(state="disabled", master=jester_frame, text="Jester Item Settings", command=self.open_jester_autobuy_settings, width=286).grid(row=3, padx=5, pady=5)
        
        mari_frame = CTkFrame(master=merchant_tab)
        mari_frame.grid(row=0, column=1, sticky="n", padx=(6, 0))
        mari_title = CTkLabel(master=mari_frame, text="Mari Autobuy", font=h1).grid(row=0, padx=5)
        enable_mari_autobuy = CTkCheckBox(state="disabled", master=mari_frame, text="Enable Mari Autobuy", variable=self.tk_var_list['mari_autobuy'], onvalue="1", offvalue="0").grid(row=1, pady=5, padx=5, sticky="w")
        mari_autobuy_settings = CTkButton(state="disabled", master=mari_frame, text="Mari Item Settings", command=self.open_mari_autobuy_settings, width=284).grid(row=3, padx=5, pady=5) 

        jester_exchange_frame = CTkFrame(master=merchant_tab)
        jester_exchange_frame.grid(row=1, columnspan=2, sticky="w", pady=(6, 0), padx=(1, 0))
        jester_exchance_title = CTkLabel(master=jester_exchange_frame, text="Jester Exchange", font=h1).grid(row=0, padx=5)
        enable_jester_exchange = CTkCheckBox(state="disabled", master=jester_exchange_frame, text="Enable Jester Exchange", width=586, variable=self.tk_var_list["jester_exchange"], onvalue="1", offvalue="0").grid(row=1, padx=5, pady=5, sticky="w")
        jester_exchange_items = CTkButton(state="disabled", master=jester_exchange_frame, text="Jester Exchange Items", width=586).grid(row=2, padx=5, pady=5)

        settings_frame = CTkFrame(master=settings_tab)
        settings_frame.grid(row=0, column=0, sticky="nw", padx=(1, 0))
        general_title = CTkLabel(master=settings_frame, text="General", font=h1).grid(row=0, padx=5, columnspan=2)
        enable_vip = CTkCheckBox(master=settings_frame, text="VIP Mode", variable=self.tk_var_list["settings"]["vip_mode"], onvalue="1", offvalue="0", width=285).grid(row=1, pady=(8, 6), padx=5, sticky="w", columnspan=2)
        enable_vip_plus = CTkCheckBox(master=settings_frame, text="VIP+ Mode", variable=self.tk_var_list["settings"]["vip+_mode"], onvalue="1", offvalue="0", width=285).grid(row=2, pady=(8, 6), padx=5, sticky="w", columnspan=2)
        
        change_ui_navigation_key = CTkButton(master=settings_frame, text="Change UI Navigation Key", command=lambda: keybinds_gui.get_keybinds(self, "UI Navigation Key", config.config_data, "ui_navigation_key")).grid(row=3, column=0, padx=5, pady=5, sticky="w")

        change_actions_button = CTkButton(master=settings_frame, text="Change Actions", command=lambda: actions_settings_gui.open_actions_settings(self), width=131).grid(row=3, column=1, padx=(1, 5), pady=5, sticky="w")
        
        themes = []
        for theme in config.config_data["themes"]:
            themes.append(theme)
        themes.append("Custom Theme")
        
        change_themes = CTkOptionMenu(master=settings_frame, values=themes, width=288, command=self.change_theme)
        change_themes.grid(row=4, padx=5, pady=5, sticky="w", columnspan=2)

        if not "/" in config.config_data["paths"]["theme"]:
            change_themes.set(config.config_data["paths"]["theme"])
        else:
            change_themes.set("Custom Theme")

        keybinds_frame = CTkFrame(master=settings_tab)
        keybinds_frame.grid(row=0, column=1, sticky="nw", padx=(5, 0))
        keybinds_title = CTkLabel(master=keybinds_frame, text="Change Keybinds", font=h1).grid(row=1)
        self.start_keybind = CTkButton(master=keybinds_frame, text=f'Change Start Keybind ({config.config_data["system_keybinds"]["start"]})', width=200, command=self.update_start_keybind)
        self.start_keybind.grid(row=2, padx=5, pady=5)
        self.stop_keybind = CTkButton(master=keybinds_frame, text=f'Change Stop Keybind ({config.config_data["system_keybinds"]["stop"]})', width=200, command=self.update_stop_keybind)
        self.stop_keybind.grid(row=4, padx=5, pady=5)

        aura_recording_frame = CTkFrame(master=extras_tab)
        aura_recording_frame.grid(row=0, column=0, sticky="n", pady=(0, 5), padx=(1, 0))
        aura_recording_title = CTkLabel(master=aura_recording_frame, text="Aura Recording", font=h1).grid(row=0, padx=5, columnspan=2)
        enable_aura_recording = CTkCheckBox(state="disabled", master=aura_recording_frame, text="Enable Aura Recording", variable=self.tk_var_list["aura_recording"]["enabled"], onvalue="1", offvalue="0").grid(row=1, padx=5, pady=5, sticky="w")
        
        aura_recording_entry_frame = CTkFrame(master=aura_recording_frame, fg_color=config.read_theme("CTkFrame")["fg_color"])
        aura_recording_entry_frame.grid(row=2, column=0, sticky="w", padx=5, pady=5, columnspan=2)

        aura_recording_minimum_label = CTkLabel(master=aura_recording_entry_frame, text="Minimum: ", justify="left").grid(row=0, column=0, sticky="w")
        self.aura_recording_minimum = CTkEntry(state="disabled", master=aura_recording_entry_frame, width=280, validate='all', validatecommand=(self.register(lambda char: char.isdigit()), '%P'))
        self.aura_recording_minimum.insert(0, config.config_data["aura_recording"]["minimum"])
        self.aura_recording_minimum.bind(command=self.update_aura_recording_minimum, sequence="<Return>")
        self.aura_recording_minimum.grid(row=0, column=1, columnspan=2, sticky="w")

        self.aura_recording_keybind_label = CTkLabel(master=aura_recording_frame, text=f'Current Keybind: {config.config_data["aura_recording"]["keybind"]}')
        self.aura_recording_keybind_label.grid(row=3, column=0, padx=(5, 0), pady=5, sticky="w")
        update_aura_recording_keybind = CTkButton(state="disabled", master=aura_recording_frame, text="Update keybinds", command=self.update_aura_recording_keybind, width=180).grid(row=3, column=1, padx=(0, 5), pady=5, sticky="w")
    
        credits_frame = CTkFrame(master=credits_tab)
        credits_frame.grid(row=0, column=0, padx=(1, 0))    
        credits_title = CTkLabel(master=credits_frame, text="Credits Team", font=h1).grid(row=0, padx=5, columnspan=3)

        message_text = """Thanks for using our macro! 
This took a long time to build and test. 
Here are some of the people responsible
for this beautiful creation."""

        credits_text = """Co-Owners:
noteab | steve | Curious Pengu

Developers: 
innocenthuman | bored man

Graphical Designer: 
CATE"""
        
        team_logo_image = CTkImage(dark_image=config.round_corners(Image.open(f"{config.parent_path()}/data/images/team_logo.png"), 35), size=(150, 150))
        logo_image = CTkImage(dark_image=config.round_corners(Image.open(f"{config.parent_path()}/data/images/logo.png"), 35), size=(150, 150))
        
        credits_label = CTkLabel(master=credits_frame, text=credits_text).grid(row=1, column=1, rowspan=2, padx=56, pady=(17, 30), sticky="n")

        logo_image_label = CTkLabel(master=credits_frame, image=logo_image, text="").grid(row=1, column=0, padx=6, pady=(0, 6))
        team_image_label = CTkLabel(master=credits_frame, image=team_logo_image, text="").grid(row=1, column=2, padx=6, pady=(0, 6))

    def on_close(self):
        config.save_tk_list(self.tk_var_list)
        self.destroy()

    def start(self, keybind=""):
        config.save_tk_list(self.tk_var_list)
        config.save_config(config.config_data)
        if main_loop.running == False:
            self.iconify()
        main_loop.start()

    def stop(self, keybind=""):
        config.save_tk_list(self.tk_var_list)
        config.save_config(config.config_data)
        if main_loop.running == True:
            self.deiconify()
        main_loop.stop()
    
    def restart(self, keybind=""):
        os.execv(sys.executable, ['python', f'"{sys.argv[0]}"'])
        self.on_close()
        sys.exit()

    def update_entry(self):
        pass
    
    def change_theme(self, choice):
        if choice == "Custom Theme":
            self.iconify()
            filepath = filedialog.askopenfilename(initialdir = "/",
                title = "Choose a theme",
                filetypes = [("Json Theme File", "*.json*")]
            )
            config.config_data["paths"]["theme"] = filepath
            config.save_config(config.config_data)
        else:
            self.tk_var_list["paths"]["theme"] = choice
            config.save_tk_list(self.tk_var_list)
        self.restart()

    def update_start_keybind(self):
        config.save_tk_list(self.tk_var_list)
        config.config_data = config.read_config()
        keybinds_gui.get_keybinds(self, "Start Macro", config.config_data["system_keybinds"], "start")
        threading.Thread(target=self.update_start_label).start()


    def update_stop_keybind(self):
        config.save_tk_list(self.tk_var_list)
        config.config_data = config.read_config()
        keybinds_gui.get_keybinds(self, "Stop Macro", config.config_data["system_keybinds"], "stop")
        threading.Thread(target=self.update_stop_label).start()

    
    def update_start_label(self):
        original_keybind = config.config_data["system_keybinds"]["start"]
        keyboard.remove_hotkey(original_keybind)
        while original_keybind == config.config_data["system_keybinds"]["start"]:
            sleep(0.1)
            pass
        self.start_keybind.configure(text=f'Change Start Keybind ({config.config_data["system_keybinds"]["start"].upper()})')
        self.start_button.configure(text=f'Start ({config.config_data["system_keybinds"]["start"].upper()})')        
        keyboard.add_hotkey(config.config_data["system_keybinds"]["start"], self.start)
        

    def update_stop_label(self):
        original_keybind = config.config_data["system_keybinds"]["stop"]
        keyboard.remove_hotkey(original_keybind)
        while original_keybind == config.config_data["system_keybinds"]["stop"]:
            sleep(0.1)
            pass
        self.stop_keybind.configure(text=f'Change Stop Keybind ({config.config_data["system_keybinds"]["stop"].upper()})')
        self.stop_button.configure(text=f'Stop ({config.config_data["system_keybinds"]["stop"].upper()})')
        keyboard.add_hotkey(config.config_data["system_keybinds"]["stop"], self.stop)


    def update_aura_recording_keybind(self):
        if self.tk_var_list["auto_equip"]["enabled"].get() == "1":
            config.save_tk_list(self.tk_var_list)
            config.config_data = config.read_config()
            keybinds_gui.get_keybinds(self, "Aura Recording", config.config_data["aura_recording"], "keybind")
            threading.Thread(target=self.update_aura_recording_label).start()
        else:
            ctypes.windll.user32.MessageBoxW(0, "Enable Auto Equip first!", "Error", 0)

    def update_aura_recording_label(self):
        original_keybind = config.config_data["aura_recording"]["keybind"]
        while original_keybind == config.config_data["aura_recording"]["keybind"]:
            sleep(0.1)
            pass # WAIT
        self.aura_recording_keybind_label.configure(text=f'Current Keybind: {config.config_data["aura_recording"]["keybind"].upper()}')

    def open_jester_autobuy_settings(self):
        from data.merchant import jester_autobuy_gui

    def open_mari_autobuy_settings(self):
        from data.merchant import mari_autobuy_gui

    def open_discord_bot_settings(self):
        from data.discord_bot import discord_bot_gui
    
    def open_add_discord_bot(self):
        from data.discord_bot import discord_bot_gui
        # run discord bot

    def open_discord_webhook_settings(self):
        from data.discord_webhook import discord_webhook_gui
        # run discord webhook settings

    def open_add_discord_webhook(self):
        from data.discord_webhook import discord_webhook_gui
        #run discord webhook gui

    def open_cycle_auto_add_settings(self):
        from data.cycle_auto_add import cycle_auto_add_gui
        # Run cycle_auto_add_gui

    def open_automatic_item_crafting_settings(self):
        from data.item_crafting import item_crafting_gui
        # Run item_crafting_gui

    def update_aura_recording_minimum(self, keypress_event):
        if self.tk_var_list["aura_recording"]["enabled"].get() == "1":
            config.save_tk_list(self.tk_var_list)
            config.config_data["aura_recording"]["minimum"] = self.aura_recording_minimum.get()
            config.save_config(config.config_data)
        else:
            ctypes.windll.user32.MessageBoxW(0, "Enable Aura Recording first!", "Error", 0)

    def update_auto_equip_aura(self, keypress_event):
        if self.tk_var_list["auto_equip"]["enabled"].get() == "1":
            config.save_tk_list(self.tk_var_list)
            config.config_data = config.read_config()

            config.config_data["auto_equip"]["aura"] = self.auto_equip_aura.get() 
            config.save_config(config.config_data)
        else:
            ctypes.windll.user32.MessageBoxW(0, "Enable Auto Equip first!", "Error", 0)
    
    def update_auto_reconnect_ps_link(self, keypress_event):
        if self.tk_var_list["auto_reconnect"]["enabled"].get() == "1":
            config.save_tk_list(self.tk_var_list)
            config.config_data = config.read_config()
            ps_link = self.ps_link.get()
            # TODO CHECK PS LINK PLS
            config.config_data["ps_link"] = ps_link
            config.save_config(config.config_data)
        else:
            ctypes.windll.user32.MessageBoxW(0, "Enable Auto Recconect first!", "Error", 0)

    def update_theme(self):
        selected_theme = self.theme_var.get()

        if selected_theme == 1:
            config.config_data["dark_mode"] = True
            config.config_data["vibrant_mode"] = False
            set_appearance_mode("dark")
        elif selected_theme == 2:
            config.config_data["dark_mode"] = False
            config.config_data["vibrant_mode"] = True
            set_appearance_mode("vibrant")  # Ensure you have defined "vibrant" in your theme settings
        else:
            config.config_data["dark_mode"] = False
            config.config_data["vibrant_mode"] = False
            set_appearance_mode("light")

        config.save_config(config.config_data)

        self.restart_app()  # Restart the app to apply the changes
    
    def focus_widget(self, event):
        try:
            event.widget.focus_set()
        except:
            pass

    def reload_config_data(self):
        config.config_data = config.read_config()
        self.tk_var_list = config.generate_tk_list()

    # def convert_keybind(self, keybinds):
    #     for keybind in keybinds.split(" + "):
    #         final_keybind = "<"
    #         final_keybind += f"{keybind}-"
    #         final_keybind += ">"
    #     return final_keybind
