import ctypes
from time import sleep
try:
    from data.lib import config
except:
    ctypes.windll.user32.MessageBoxW(0, "Why the fuck are you running this file?\nWho told you to run this?", "Error", 0)
    exit(1)

from data.keybinds import keybinds_gui
from data.main_loop import main_loop
from customtkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import threading
import json
from data.lib.ahk import ahk


CURRENT_VERSION = config.get_current_version()
DEFAULT_FONT = "Segoe UI"
DEFAULT_FONT_BOLD = "Segoe UI Semibold"
MAX_WIDTH = 1000

class MainWindow(CTk):
    def __init__(self):
        super().__init__()
        self.bind_all("<Button-1>", self.focus_widget)
        self.config_data = config.read_config()
        self.title(f"Radiance Macro v{CURRENT_VERSION}")
        self.geometry("630x315x200x200")
        self.resizable(False, False)
        self.grid_columnconfigure(0, weight=1)
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.iconpath = ImageTk.PhotoImage(file=f"{config.parent_path()}/data/images/tray_radiant.png")
        self.wm_iconbitmap()
        self.iconphoto(False, self.iconpath)
        
        self.aura_recording_keybind_window = None
        self.tk_var_list = config.generate_tk_list()

        set_default_color_theme(f"{self.config_data["parent_path"]}{config.theme_path()}")

        set_appearance_mode("dark") # NO MORE LIGHT MODE IT IS ABSOLUTELY DOGGY DOO DOO

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

        self.start_button = CTkButton(master=system_button_frame, text=f"Start ({self.config_data["start_keybind"]})", command=self.start, height=30, width=100, corner_radius=4)
        self.start_button.grid(row=0, column=0, padx=4, pady=4)
        
        self.stop_button = CTkButton(master=system_button_frame, text=f"Stop ({self.config_data["stop_keybind"]})", command=self.stop, height=30, width=100, corner_radius=4)
        self.stop_button.grid(row=0, column=2, padx=4, pady=4)

        # TODO
        ahk.add_hotkey(self.config_data["stop_keybind"], self.stop)
        ahk.add_hotkey(self.config_data["start_keybind"], self.start)
        ahk.add_hotkey("F3", self.restart)

        # FONTS
        h1 = CTkFont(DEFAULT_FONT_BOLD, size=20, weight="bold")
        h2 = CTkFont(DEFAULT_FONT_BOLD, size=15, weight="bold")

        text = CTkFont(DEFAULT_FONT, size=12, weight="normal")

        obby_frame = CTkFrame(master=main_tab)
        obby_frame.grid(row=0, column=0, sticky="n", padx=(1, 1))
        obby_title_label = CTkLabel(master=obby_frame, text="Obby", font=h1).grid(row=0, column=1)
        do_obby_checkbox = CTkCheckBox(master=obby_frame, text="Do Obby (30% Luck Boost Every 2 Mins)", variable=self.tk_var_list["do_obby"], onvalue="1", offvalue="0").grid(row=2, column=1, padx=5, pady=5, stick="w")
        check_for_obby_buff_check_box = CTkCheckBox(master=obby_frame, text="Check for Obby Buff Effect", variable=self.tk_var_list["check_for_obby_buff"], onvalue="1", offvalue="0").grid(row=3, column=1, padx=5, pady=5, stick="w")

        auto_equip_frame = CTkFrame(master=main_tab, width=200, height=31)
        auto_equip_frame.grid(row=0, column=1, stick="n", padx=(5, 0))
        auto_equip_title = CTkLabel(master=auto_equip_frame, text="Auto Equip", font=h1).grid(row=0, pady=(0, 3), columnspan=2)

        enable_auto_equip = CTkCheckBox(master=auto_equip_frame, text="Enable Auto Equip", variable=self.tk_var_list["auto_equip"], onvalue="1", offvalue="0").grid(row=1, pady=(1, 6), sticky="w", padx=(5, 4))
        self.auto_equip_aura = CTkEntry(master=auto_equip_frame, placeholder_text="Aura", width=330)
        self.auto_equip_aura.bind(command=self.update_auto_equip_aura, sequence="<Return>")
        if not self.config_data["auto_equip_aura"] == "":
            self.auto_equip_aura.insert(0, self.config_data["auto_equip_aura"])
            
        
        self.auto_equip_aura.grid(row=2, column=0, padx=5, sticky="e", pady=(0, 6))

        paths_frame = CTkFrame(master=main_tab)
        paths_frame.grid(row=1, pady=(6, 0), column=0, padx=(1, 0))
        
        paths_title = CTkLabel(master=paths_frame, text="Paths", font=h1, width=240).grid(row=0, padx=5)

        enable_collect_items = CTkCheckBox(master=paths_frame, text="Enable Item Collection", variable=self.tk_var_list["collect_items"], onvalue="1", offvalue="0").grid(row=1, sticky="w", padx=5, pady=5)
        autograil = CTkCheckBox(master=paths_frame, text="Auto grail", variable=self.tk_var_list["30_fps_path"], onvalue="1", offvalue="0").grid(row=2, sticky="w", padx=5, pady=5)
        
        # CTkCheckBox(master=spot_collection_frame, text='1', width=45, variable=self.tk_var_list['collect_spot_1'], onvalue='1', offvalue='0').grid(row=1, column=0, sticky='e', padx=(5, 0))
        # for i in range(1, 8):
        #     exec(f"CTkCheckBox(master=spot_collection_frame, text='{i + 1}', width=45, variable=self.tk_var_list['collect_spot_{i + 1}'], onvalue='1', offvalue='0').grid(row=1, column={i}, sticky='e')")

        reconnect_frame = CTkFrame(master=main_tab, width=200, height=31)
        reconnect_frame.grid(row=1, column=1, stick="n", padx=(5, 0), pady=(6, 0))
        reconnect_title = CTkLabel(master=reconnect_frame, text="Auto reconnect", font=h1).grid(row=0, pady=(0, 3))
    
        enable_reconnect = CTkCheckBox(master=reconnect_frame, text="Enable Auto reconnect", variable=self.tk_var_list["auto_reconnect"], onvalue="1", offvalue="0").grid(row=1, pady=(1, 6), sticky="w", padx=(5, 4))
        self.ps_link = CTkEntry(master=reconnect_frame, placeholder_text="Private Server Link", width=330)
        self.ps_link.bind(command=self.update_auto_reconnect_ps_link, sequence="<Return>")
        if not self.config_data["ps_link"] == "":
            self.ps_link.insert(0, self.config_data["ps_link"])
        self.ps_link.grid(row=2, column=0, padx=5, sticky="e", pady=(0, 6))

        item_crafting_frame = CTkFrame(master=crafting_tab)
        item_crafting_frame.grid(row=0, column=0, padx=(1, 0))
        item_crafting_title = CTkLabel(master=item_crafting_frame, text="Automatic Item Crafting", font=h1).grid(row=0, padx=5)
        enable_item_crafting_checkbox = CTkCheckBox(master=item_crafting_frame, text="Enable Automatic Item Crafting", variable=self.tk_var_list["automatic_item_crafting"], onvalue='1', offvalue='0').grid(row=1, padx=5, pady=5, sticky="w")
        item_crafting_settings_button = CTkButton(master=item_crafting_frame, text="Automatic Item Crafting Settings", command=self.open_automatic_item_crafting_settings, width=286).grid(padx=5, pady=5)

        potion_crafting_frame = CTkFrame(master=crafting_tab)
        potion_crafting_frame.grid(row=0, column=1, padx=(6, 5), sticky="n")
        potion_crafting_title = CTkLabel(master=potion_crafting_frame, text="Automatic Potion Crafting", font=h1).grid(row=0, padx=5)
        enable_potion_crafting_checkbox = CTkCheckBox(master=potion_crafting_frame, text="Enable Automatic Potion Crafting", variable=self.tk_var_list["automatic_potion_crafting"], onvalue='1', offvalue='0').grid(row=1, padx=5, pady=5, sticky="w")
        potion_crafting_settings_button = CTkButton(master=potion_crafting_frame, text="Automatic Potion Crafting Settings", width=284, command=self.open_automatic_potion_crafting_settings).grid(row=2, padx=5, pady=5)

        cycle_auto_add_settings_frame = CTkFrame(master=crafting_tab)
        cycle_auto_add_settings_frame.grid(row=1, columnspan=2, sticky="w", pady=(6, 0), padx=(1, 0))
        switch_auto_add_title = CTkLabel(master=cycle_auto_add_settings_frame, text='Cycle "Auto Add"', font=h1).grid(row=0)
        enable_switch_auto_add_checkbox = CTkCheckBox(master=cycle_auto_add_settings_frame, text='Enable Cycle "Auto Add" (For both Potion Crafting and Item Crafting)', variable=self.tk_var_list["cycle_auto_add"], onvalue="1", offvalue="0").grid(row=1, padx=5, sticky="w", pady=5)
        cycle_auto_add_settings = CTkButton(master=cycle_auto_add_settings_frame, text="Cycle Auto Add Settings", command=self.open_automatic_potion_crafting_settings, width=586).grid(row=2, padx=5, pady=5)

        discord_webhook_frame = CTkFrame(master=discord_tab)
        discord_webhook_frame.grid(row=0, column=0, sticky="n", pady=(0, 0), padx=(1, 0))
        discord_webhook_title = CTkLabel(master=discord_webhook_frame, text="Discord Webhooks", font=h1).grid(row=0, padx=5)
        enable_discord_webhook = CTkCheckBox(master=discord_webhook_frame, text="Enable Discord Webhooks", variable=self.tk_var_list['discord_webhook'], onvalue="1", offvalue="0").grid(row=1, padx=5, pady=5, sticky="w")
        discord_webhook_list = CTkButton(master=discord_webhook_frame, text="Add Discord Webhook", command=self.open_add_discord_webhook, width=286).grid(row=2, padx=5, pady=5)
        discord_webhook_settings = CTkButton(master=discord_webhook_frame, text="Discord Webhook Settings", command=self.open_discord_webhook_settings, width=286).grid(row=3, padx=5, pady=5)
        
        discord_bot_frame = CTkFrame(master=discord_tab)
        discord_bot_frame.grid(row=0, column=1, sticky="n", pady=(0, 0), padx=(6, 0))
        discord_bot_title = CTkLabel(master=discord_bot_frame, text="Discord Bot", font=h1).grid(row=0, padx=5)
        enable_discord_bot = CTkCheckBox(master=discord_bot_frame, text="Enable Discord Bot", variable=self.tk_var_list["discord_bot"], onvalue="1", offvalue="0").grid(row=1, padx=5, pady=5, sticky="w")
        add_discord_bot_button = CTkButton(master=discord_bot_frame, text="Add Discord Bot", command=self.open_add_discord_bot, width=285).grid(row=2, padx=5, pady=5)
        discord_bot_settings_button = CTkButton(master=discord_bot_frame, text="Discord Bot Settings", command=self.open_discord_bot_settings, width=285).grid(row=3, padx=5, pady=5)

        community_frame = CTkFrame(master=discord_tab)
        community_frame.grid(row=1, columnspan=2, pady=(6, 0), padx=(1, 0), sticky="n")
        community_title = CTkLabel(master=community_frame, text="Community", font=h1, width=586).grid(row=0, padx=5)
        coming_soon = CTkLabel(master=community_frame, text="Website Coming Soon", width=586).grid(row=1, padx=5, pady=(3, 3))

        jester_frame = CTkFrame(master=merchant_tab)
        jester_frame.grid(row=0, column=0, sticky="n", padx=(1, 0))
        jester_title = CTkLabel(master=jester_frame, text="Jester Autobuy", font=h1).grid(row=0, padx=5)
        enable_jester_autobuy = CTkCheckBox(master=jester_frame, text="Enable Jester Autobuy", variable=self.tk_var_list['jester_autobuy'], onvalue="1", offvalue="0").grid(row=1, pady=5, padx=5, sticky="w")
        jester_item_settings = CTkButton(master=jester_frame, text="Jester Item Settings", command=self.open_jester_autobuy_settings, width=286).grid(row=3, padx=5, pady=5)
        
        mari_frame = CTkFrame(master=merchant_tab)
        mari_frame.grid(row=0, column=1, sticky="n", padx=(6, 0))
        mari_title = CTkLabel(master=mari_frame, text="Mari Autobuy", font=h1).grid(row=0, padx=5)
        enable_mari_autobuy = CTkCheckBox(master=mari_frame, text="Enable Mari Autobuy", variable=self.tk_var_list['mari_autobuy'], onvalue="1", offvalue="0").grid(row=1, pady=5, padx=5, sticky="w")
        mari_autobuy_settings = CTkButton(master=mari_frame, text="Mari Item Settings", command=self.open_mari_autobuy_settings, width=284).grid(row=3, padx=5, pady=5) 

        jester_exchange_frame = CTkFrame(master=merchant_tab)
        jester_exchange_frame.grid(row=1, columnspan=2, sticky="w", pady=(6, 0), padx=(1, 0))
        jester_exchance_title = CTkLabel(master=jester_exchange_frame, text="Jester Exchange", font=h1).grid(row=0, padx=5)
        enable_jester_exchange = CTkCheckBox(master=jester_exchange_frame, text="Enable Jester Exchange", width=586, variable=self.tk_var_list["jester_exchange"], onvalue="1", offvalue="0").grid(row=1, padx=5, pady=5, sticky="w")
        jester_exchange_items = CTkButton(master=jester_exchange_frame, text="Jester Exchange Items", width=586).grid(row=2, padx=5, pady=5)

        settings_frame = CTkFrame(master=settings_tab)
        settings_frame.grid(row=0, column=0, sticky="nw", padx=(1, 0))
        general_title = CTkLabel(master=settings_frame, text="General", font=h1).grid(row=0, padx=5)
        enable_vip = CTkCheckBox(master=settings_frame, text="VIP Mode", variable=self.tk_var_list["vip_mode"], onvalue="1", offvalue="0", width=285).grid(row=1, pady=5, padx=5, sticky="w")

        keybinds_frame = CTkFrame(master=settings_tab)
        keybinds_frame.grid(row=0, column=1, sticky="nw", padx=(5, 0))
        keybinds_title = CTkLabel(master=keybinds_frame, text="Change Keybinds", font=h1).grid(row=1)
        self.start_keybind = CTkButton(master=keybinds_frame, text=f"Change Start Keybind ({self.config_data["start_keybind"]})", width=200, command=self.update_start_keybind)
        self.start_keybind.grid(row=2, padx=5, pady=5)
        self.stop_keybind = CTkButton(master=keybinds_frame, text=f"Change Stop Keybind ({self.config_data["stop_keybind"]})", width=200, command=self.update_stop_keybind)
        self.stop_keybind.grid(row=4, padx=5, pady=5)

        aura_recording_frame = CTkFrame(master=extras_tab)
        aura_recording_frame.grid(row=0, column=0, sticky="n", pady=(0, 5), padx=(1, 0))
        aura_recording_title = CTkLabel(master=aura_recording_frame, text="Aura Recording", font=h1).grid(row=0, padx=5, columnspan=2)
        enable_aura_recording = CTkCheckBox(master=aura_recording_frame, text="Enable Aura Recording", variable=self.tk_var_list["aura_recording"], onvalue="1", offvalue="0").grid(row=1, padx=5, pady=5, sticky="w")
        
        aura_recording_entry_frame = CTkFrame(master=aura_recording_frame, fg_color=config.read_theme("CTkFrame")["fg_color"])
        aura_recording_entry_frame.grid(row=2, column=0, sticky="w", padx=5, pady=5, columnspan=2)

        aura_recording_minimum_label = CTkLabel(master=aura_recording_entry_frame, text="Minimum: ", justify="left").grid(row=0, column=0, sticky="w")
        self.aura_recording_minimum = CTkEntry(master=aura_recording_entry_frame, width=280, validate='all', validatecommand=(self.register(lambda char: char.isdigit()), '%P'))
        self.aura_recording_minimum.insert(0, self.config_data["aura_recording_minimum"])
        self.aura_recording_minimum.bind(command=self.update_aura_recording_minimum, sequence="<Return>")
        self.aura_recording_minimum.grid(row=0, column=1, columnspan=2, sticky="w")

        self.aura_recording_keybind_label = CTkLabel(master=aura_recording_frame, text=f"Current Keybind: {self.config_data["aura_recording_keybind"]}")
        self.aura_recording_keybind_label.grid(row=3, column=0, padx=(5, 0), pady=5, sticky="w")
        update_aura_recording_keybind = CTkButton(master=aura_recording_frame, text="Update keybinds", command=self.update_aura_recording_keybind, width=180).grid(row=3, column=1, padx=(0, 5), pady=5, sticky="w")
        
    
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
innocenthuman | bored man | Allan | TheEndyy

Graphical Designer: 
CATE"""
        
        team_logo_image = CTkImage(dark_image=config.round_corners(Image.open(f"{config.parent_path()}/data/images/team_logo.png"), 35), size=(150, 150))
        logo_image = CTkImage(dark_image=config.round_corners(Image.open(f"{config.parent_path()}/data/images/logo.png"), 35), size=(150, 150))
        
        credits_label = CTkLabel(master=credits_frame, text=credits_text).grid(row=1, column=1, rowspan=2, padx=10, pady=(17, 30), sticky="n")

        logo_image_label = CTkLabel(master=credits_frame, image=logo_image, text="").grid(row=1, column=0, padx=6, pady=(0, 6))
        team_image_label = CTkLabel(master=credits_frame, image=team_logo_image, text="").grid(row=1, column=2, padx=6, pady=(0, 6))
        ahk.start_hotkeys()

    def on_close(self):
        config.save_tk_list(self.tk_var_list)
        self.destroy()

    def start(self, keybind=""):
        config.save_tk_list(self.tk_var_list)
        config.save_config(self.config_data)
        if main_loop.running == False:
            self.iconify()
        main_loop.start()

    def stop(self, keybind=""):
        config.save_tk_list(self.tk_var_list)
        config.save_config(self.config_data)
        if main_loop.running == True:
            self.deiconify()
        main_loop.stop()
    
    def restart(self, keybind=""):
        os.execv(sys.executable, ['python', f'"{sys.argv[0]}"'])
        self.on_close()
        sys.exit()

    def update_entry(self):
        pass
    
    def update_start_keybind(self):
        config.save_tk_list(self.tk_var_list)
        self.config_data = config.read_config()
        keybinds_gui.get_keybinds(self, "Start Macro", "start_keybind")
        threading.Thread(target=self.update_start_label).start()


    def update_stop_keybind(self):
        config.save_tk_list(self.tk_var_list)
        self.config_data = config.read_config()
        keybinds_gui.get_keybinds(self, "Stop Macro", "stop_keybind")
        threading.Thread(target=self.update_stop_label).start()

    
    def update_start_label(self):
        original_keybind = self.config_data["start_keybind"]
        ahk.remove_hotkey(original_keybind)
        while original_keybind == self.config_data["start_keybind"]:
            sleep(0.1)
            pass
        self.start_keybind.configure(text=f"Change Start Keybind ({self.config_data["start_keybind"].upper()})")
        self.start_button.configure(text=f"Start ({self.config_data["start_keybind"].upper()})")        
        ahk.add_hotkey(self.config_data["start_keybind"], self.start)
        

    def update_stop_label(self):
        original_keybind = self.config_data["stop_keybind"]
        ahk.remove_hotkey(original_keybind)
        while original_keybind == self.config_data["stop_keybind"]:
            sleep(0.1)
            pass
        self.stop_keybind.configure(text=f"Change Stop Keybind ({self.config_data["stop_keybind"].upper()})")
        self.stop_button.configure(text=f"Stop ({self.config_data["stop_keybind"].upper()})")
        ahk.add_hotkey(self.config_data["stop_keybind"], self.stop)


    def update_aura_recording_keybind(self):
        if self.tk_var_list["auto_equip"].get() == "1":
            config.save_tk_list(self.tk_var_list)
            self.config_data = config.read_config()
            keybinds_gui.get_keybinds(self, "Aura Recording", "aura_recording_keybind")
            threading.Thread(target=self.update_aura_recording_label).start()
        else:
            messagebox.showwarning(title="Warning", message="Enable Auto Equip first!")

    def update_aura_recording_label(self):
        original_keybind = self.config_data["aura_recording_keybind"]
        while original_keybind == self.config_data["aura_recording_keybind"]:
            sleep(0.1)
            pass # WAIT
        self.aura_recording_keybind_label.configure(text=f"Current Keybind: {self.config_data["aura_recording_keybind"].upper()}")

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

    def open_automatic_potion_crafting_settings(self):
        from data.potion_crafting import potion_crafting_gui
        # Run potion_crafting_gui

    def open_automatic_item_crafting_settings(self):
        from data.item_crafting import item_crafting_gui
        # Run item_crafting_gui

    def update_aura_recording_minimum(self, keypress_event):
        if self.tk_var_list["aura_recording"].get() == "1":
            config.save_tk_list(self.tk_var_list)
            self.config_data["aura_recording_minimum"] = self.aura_recording_minimum.get()
            config.save_config(self.config_data)
        else:
            messagebox.showwarning(title="Warning", message="Enable Aura Recording first!")

    def update_auto_equip_aura(self, keypress_event):
        if self.tk_var_list["auto_equip"].get() == "1":
            config.save_tk_list(self.tk_var_list)
            self.config_data = config.read_config()

            self.config_data["auto_equip_aura"] = self.auto_equip_aura.get() 
            config.save_config(self.config_data)
        else:
            messagebox.showwarning(title="Warning", message="Enable Auto Equip first!")
    
    def update_auto_reconnect_ps_link(self, keypress_event):
        if self.tk_var_list["auto_reconnect"].get() == "1":
            config.save_tk_list(self.tk_var_list)
            self.config_data = config.read_config()
            ps_link = self.ps_link.get()
            # TODO CHECK PS LINK PLS
            self.config_data["ps_link"] = ps_link
            config.save_config(self.config_data)
        else:
            messagebox.showwarning(title="Warning", message="Enable Auto Reconnect first!")

    def update_theme(self):
        selected_theme = self.theme_var.get()

        if selected_theme == 1:
            self.config_data["dark_mode"] = True
            self.config_data["vibrant_mode"] = False
            set_appearance_mode("dark")
        elif selected_theme == 2:
            self.config_data["dark_mode"] = False
            self.config_data["vibrant_mode"] = True
            set_appearance_mode("vibrant")  # Ensure you have defined "vibrant" in your theme settings
        else:
            self.config_data["dark_mode"] = False
            self.config_data["vibrant_mode"] = False
            set_appearance_mode("light")

        config.save_config(self.config_data)

        self.restart_app()  # Restart the app to apply the changes
    
    def focus_widget(self, event):
        try:
            event.widget.focus_set()
        except:
            pass

    def reload_config_data(self):
        self.config_data = config.read_config()
        self.tk_var_list = config.generate_tk_list()

    # def convert_keybind(self, keybinds):
    #     for keybind in keybinds.split(" + "):
    #         final_keybind = "<"
    #         final_keybind += f"{keybind}-"
    #         final_keybind += ">"
    #     return final_keybind
