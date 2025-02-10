# Radiance Macro © 2024 by Radiant Team is licensed under Creative Commons Attribution-ShareAlike 4.0 International

import sys
import ctypes
import pathlib

sys.dont_write_bytecode = True
sys.path.append(pathlib.Path(__file__).parent.resolve())

# def download_easyocr_model():
#     """Run a basic EasyOCR script to download the recognition model."""
#     import easyocr

#     reader = easyocr.Reader(['en'])  # Create a reader instance
#     print("EasyOCR model downloaded successfully.")

def run_update_checker():
    """Run the update checker"""
    try:
        from update_checker import update_checker
    except ImportError as e:
        ctypes.windll.user32.MessageBoxW(0, f"IMPORT ERROR\nError: {e}", "Error", 0)
    update_checker.check_for_updates()
    

def set_path():
    # try:
    #     from lib import config
    # except ImportError:
    #     ctypes.windll.user32.MessageBoxW(0, "CONFIG FILE NOT FOUND", "Error", 0)
    with open(".p.txt", "w", encoding="utf-8") as file:
        file.write(str(pathlib.Path(__file__).parent.parent.resolve()))

def main():
    # check_and_install_modules()
    # """Main function to check if it's the first time running the installer."""
    # if not os.path.exists('installer_status.json'):
    #     download_easyocr_model()
    #     # Create a file to indicate the installation has occurred
    #     with open('installer_status.json', 'w') as f:
    #         json.dump({"installed": True}, f)

    print("[INITIALIZING]")
    set_path()
    run_update_checker()
    from lib import config
    from lib import window
    version = config.get_current_version()
    if window.check_radiance_windows() == True and not ("beta" in version or "alpha" in version):
        if ctypes.windll.user32.MessageBoxW(0, "Radiance Already Open!\nDo you wish to continue?", "Warning", 4) == 7:
            quit()
    
    from main_loop import main_loop
    main_loop.start_keybinds()

if __name__ == "__main__":
    main()
