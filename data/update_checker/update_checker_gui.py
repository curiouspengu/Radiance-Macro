import webbrowser

from customtkinter import *

DEFAULT_FONT = "Segoe UI"
DEFAULT_FONT_BOLD = "Segoe UI Semibold"

class UpdateWindow(CTk):
    def __init__(self, update, is_beta, current_version="", latest_version=""):
        super().__init__()
        try:
            from data.lib import config
            self.after(196, lambda: self.wm_iconbitmap(f"{config.parent_path()}/data/images/tray_radiant.ico"))
        except:
            pass
        self.geometry("500x160")
        h2 = CTkFont(DEFAULT_FONT, size=17)
        self.resizable(False, False)
        set_default_color_theme(config.theme_path())
        self.configure(fg_color=config.read_theme("CTk")["fg_color"])
        
        if update == True:
            self.title("You can update!")

            update_label = CTkLabel(master=self, text=f"You can update!", font=CTkFont(DEFAULT_FONT_BOLD, size=30, weight="bold")).pack()

            current_version_label = CTkLabel(master=self, text=f"Your current version: v{current_version}", font=h2).pack()
            latest_version_label = CTkLabel(master=self, text=f"Latest version: v{latest_version}", font=h2).pack()
            github_link_button = CTkButton(master=self, text="Update (Recommended)", font=h2, command=self.github_link_button_event).pack(pady=(10, 0), ipady=5, ipadx=5)

        if is_beta == True and update == False:
            self.geometry("500x185")
            self.title("Beta Notice")
            beta_notice_label = CTkLabel(master=self, text="You are using an alpha/beta version of Radiance Macro. Please be advised that this version may be unstable.", font=h2, wraplength=450).pack()
            current_version_label = CTkLabel(master=self, text=f"Your current version: v{current_version}", font=CTkFont(DEFAULT_FONT, size=17, weight="bold")).pack()
            close_button = CTkButton(master=self, text="Close (Recommended)", font=h2, command=exit).pack(pady=(10, 0), ipady=5, ipadx=5)
            continue_button = CTkButton(master=self, text="Continue (Not Recommended)", font=h2, command=self.destroy).pack(pady=10, ipady=5, ipadx=5)

    def github_link_button_event(command):
        webbrowser.open("https://github.com/noteab/dolphSol-Improvement-Macro/releases/latest")
        exit()