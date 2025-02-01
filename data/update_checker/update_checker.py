from time import sleep

from lib import config

import requests

CURRENT_VERSION = config.get_current_version()
BETA_VERSION = ("beta" in CURRENT_VERSION or "alpha" in CURRENT_VERSION)
IS_DEV = ("dev" in CURRENT_VERSION)

def get_latest_release_tag():
    url = f"https://api.github.com/repos/curiouspengu/Radiance-Macro/releases"
    headers = {'Accept': 'application/vnd.github.v3+json'}
    response = requests.get(url, headers=headers)
    
    return_list = [-1, -1]
    if response.status_code == 200:
        releases = response.json()
        if releases:
            for release in releases:
                if not release["prerelease"]:
                    if return_list[0] == -1:
                        return_list[0] = release['tag_name']
                else:
                    if return_list[1] == -1:
                        return_list[1] = release['tag_name']
            return return_list
        else:
            return "No releases found"
    else:
        return

def check_for_updates():
    latest_version = get_latest_release_tag()
    if IS_DEV == True:
        return
    
    if (not CURRENT_VERSION == latest_version[0]) and (not CURRENT_VERSION == latest_version[1]):
        print("You can update! Update here:\nhttps://github.com/steveonly2/Radiance-Macro/releases\n")
        print(f"Your version: {CURRENT_VERSION}")
        print(f"Latest version: {latest_version[0]}")
        print(f"Latest beta version: {latest_version[1]}\n")
        print("Wait 5 seconds.")
        sleep(5)
        input("Press enter to continue... ")

    elif CURRENT_VERSION == latest_version[1]:
        print("NOTICE: You are using a alpha/beta version of Radiance Macro. This version may be buggy.\n")