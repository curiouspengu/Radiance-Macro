# Radiance Macro © 2024 by Radiant Team is licensed under Creative Commons Attribution-ShareAlike 4.0 International

import os
import subprocess
import sys
import json
import ctypes
import pathlib
import threading

sys.dont_write_bytecode = True
sys.path.append(pathlib.Path(__file__).parent.resolve())

def download_easyocr_model():
    """Run a basic EasyOCR script to download the recognition model."""
    import easyocr

    reader = easyocr.Reader(['en'])  # Create a reader instance
    print("EasyOCR model downloaded successfully.")

def run_update_checker():
    """Run the update checker"""
    try:
        from data.update_checker import update_checker
    except ImportError:
        ctypes.windll.user32.MessageBoxW(0, "UPDATE CHECKER NOT FOUND", "Error", 0)
    update_checker.check_for_updates()
    
def create_main_gui(gui):
    """Run the main GUI script."""
    gui.mainloop()

def set_path():
    # try:
    #     from data.lib import config
    # except ImportError:
    #     ctypes.windll.user32.MessageBoxW(0, "CONFIG FILE NOT FOUND", "Error", 0)
    with open("path.txt", "w") as file:
        file.write(str(pathlib.Path(__file__).parent.resolve()))

def main():
    # check_and_install_modules()
    # """Main function to check if it's the first time running the installer."""
    # if not os.path.exists('data/installer_status.json'):
    #     download_easyocr_model()
    #     # Create a file to indicate the installation has occurred
    #     with open('data/installer_status.json', 'w') as f:
    #         json.dump({"installed": True}, f)
    set_path()
    run_update_checker()
    from data.lib import config
    from data.main_gui import main_gui
    from data.lib import window
    version = config.get_current_version()
    if window.check_radiance_windows() == True and not ("beta" in version or "alpha" in version):
        if ctypes.windll.user32.MessageBoxW(0, "Radiance Already Open!\nDo you wish to continue?", "Warning", 4) == 7:
            quit()
    gui = main_gui.MainWindow()
    create_main_gui(gui)



if __name__ == "__main__":
    main()
