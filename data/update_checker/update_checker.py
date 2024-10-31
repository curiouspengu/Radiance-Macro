from data.lib import config
from data.update_checker import update_checker_gui

CURRENT_VERSION = config.get_current_version()
BETA_VERSION = ("beta" in CURRENT_VERSION or "alpha" in CURRENT_VERSION)

def check_for_updates():
    online_config_data = config.read_remote()
    if (not CURRENT_VERSION == online_config_data["version"]) and (not CURRENT_VERSION == online_config_data["latest_beta_version"]):
        update_checker_gui.UpdateWindow(update=True, current_version=CURRENT_VERSION, latest_version=online_config_data["version"], is_beta=BETA_VERSION).mainloop()
    elif CURRENT_VERSION == online_config_data["latest_beta_version"]:
        update_checker_gui.UpdateWindow(update=False, current_version=CURRENT_VERSION, is_beta=BETA_VERSION).mainloop()