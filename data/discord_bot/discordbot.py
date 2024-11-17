import discord
import os
import json
import pygetwindow as gw
from PIL import Image
import time
import pyautogui
from ahk import AHK
import ctypes
import asyncio

# Initialize AHK for automation
ahk = AHK()

# Set up intents
intents = discord.Intents.default()
intents.message_content = True

# Path to config.json for dynamic path handling
installer_dir = os.path.join("C:", os.sep, "installer")
config_path = os.path.join(installer_dir, "config.json")

# Ensure installer directory exists
if not os.path.exists(installer_dir):
    os.makedirs(installer_dir)

# Function to load or ask for the token
def load_token():
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            config = json.load(f)
            if "token" in config:
                return config["token"]

    # Prompt for token if not found in config.json
    token = input("Please enter your Discord bot token: ")
    config = {"token": token}
    save_config(config)  # Save config with token initially
    return token

# Function to save config to config.json
def save_config(config):
    with open(config_path, "w") as f:
        json.dump(config, f, indent=4)

# Function to get the screen resolution using ctypes
def get_screen_resolution():
    user32 = ctypes.windll.user32
    screen_width = user32.GetSystemMetrics(0)  # Get screen width
    screen_height = user32.GetSystemMetrics(1)  # Get screen height
    return screen_width, screen_height

# Function to adjust coordinates based on screen resolution
def adjust_coordinates(x, y, screen_width, screen_height):
    adjusted_x = int(x * screen_width / 1920)  # Assuming 1920x1080 is the base resolution
    adjusted_y = int(y * screen_height / 1080)
    return adjusted_x, adjusted_y

# Function to check if Roblox is running
def is_roblox_open():
    windows = gw.getWindowsWithTitle("Roblox")
    for window in windows:
        if "Roblox" in window.title:
            return window
    return None

# Function to take a full-screen screenshot
def take_screenshot(filename):
    roblox_window = is_roblox_open()
    if not roblox_window:
        return None  # Return None if Roblox is not open

    # Ensure Roblox is in windowed mode and bring it to focus
    roblox_window.activate()
    time.sleep(0.5)  # Allow time for window focus

    # Take a full-screen screenshot using pyautogui
    screenshot = pyautogui.screenshot()
    screenshot.save(filename)
    return filename

# Function to press the first button again to close it
def close_button():
    # Close the opened button by pressing the first button's coordinates again
    button_coords = load_or_initialize_coordinates()  # Load coordinates
    ahk.mouse_move(*button_coords["inventory"], speed=10)
    ahk.click()
    time.sleep(1)

# Load or initialize coordinates based on screen resolution
def load_or_initialize_coordinates():
    screen_width, screen_height = get_screen_resolution()

    # Check if coordinates are already saved in config.json
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            config = json.load(f)
            if "coordinates" in config:
                return config["coordinates"]

    # Default coordinates (relative to 1920x1080 resolution)
    coordinates = {
        "inventory": adjust_coordinates(45, 540, screen_width, screen_height),
        "storage": adjust_coordinates(38, 401, screen_width, screen_height),
        "daily_quest_first": adjust_coordinates(55, 596, screen_width, screen_height),
        "daily_quest_second": adjust_coordinates(1236, 337, screen_width, screen_height),
        "screenshot_position": adjust_coordinates(884, 166, screen_width, screen_height),
        "aura_first": adjust_coordinates(56, 415, screen_width, screen_height),
        "aura_second": adjust_coordinates(879, 365, screen_width, screen_height),
        "aura_third": adjust_coordinates(825, 436, screen_width, screen_height),
        "aura_fourth": adjust_coordinates(673, 635, screen_width, screen_height)
    }

    # Save the adjusted coordinates to config.json
    config = {"token": load_token(), "coordinates": coordinates}
    save_config(config)

    return coordinates

# Function to verify the bot token is valid
async def validate_token(bot, token):
    try:
        # Try logging in to verify the token is valid
        await bot.login(token)
        return True
    except discord.errors.LoginFailure:
        return False

# Create bot instance
bot = discord.Bot(intents=intents)

# Token validation loop inside an async function
async def run_bot():
    token = load_token()  # Load the token inside the run_bot() function
    valid_token = False
    while not valid_token:
        valid_token = await validate_token(bot, token)
        if not valid_token:
            print("The token you entered is invalid. Please enter a valid token.")
            token = input("Please enter your Discord bot token: ")
            # Re-initialize the coordinates before saving
            button_coords = load_or_initialize_coordinates()
            config = {"token": token, "coordinates": button_coords}
            save_config(config)
        else:
            print("Token validated successfully.")
    
    # Once the token is validated, run the bot
    await bot.start(token)

# Screenshot command
@bot.slash_command(name="screenshot", description="Take a screenshot of inventory, storage, or daily quest.")
async def screenshot(ctx, option: str):
    await ctx.defer()  # Defer response while processing

    # Check if the user provided a valid option
    valid_options = ["inventory", "storage", "daily_quest"]
    if option.lower() not in valid_options:
        await ctx.respond(f"Invalid option. Please choose one of the following: {', '.join(valid_options)}")
        return

    # Load the coordinates from config.json
    button_coords = load_or_initialize_coordinates()

    # Determine the coordinates for the chosen option
    if option.lower() == "inventory":
        filename = take_screenshot("inventory_screenshot.png")
    elif option.lower() == "storage":
        filename = take_screenshot("storage_screenshot.png")
    elif option.lower() == "daily_quest":
        # First move to the daily quest position and click
        ahk.mouse_move(*button_coords["daily_quest_first"], speed=10)
        ahk.click()
        time.sleep(1)  # Allow time for the click action to be completed

        # Click the additional button for daily quest
        ahk.mouse_move(*button_coords["daily_quest_second"], speed=10)
        ahk.click()
        time.sleep(1)  # Allow time for the second click

        # Finally take a screenshot
        filename = take_screenshot("daily_quest_screenshot.png")

    if filename is None:
        await ctx.respond("Roblox is not open or not in focus. Please open Roblox in windowed mode.")
        return

    # Close the first button again
    close_button()

    # Send the screenshot to the user
    await ctx.respond(file=discord.File(filename))

    # Clean up the file after sending
    os.remove(filename)

# New command to equip an aura
@bot.slash_command(name="equipaura", description="Equip an aura by name.")
async def equipaura(ctx, aura_name: str):
    await ctx.defer()  # Defer response while processing

    # Load the coordinates from config.json
    button_coords = load_or_initialize_coordinates()

    # Move to the first position and click
    ahk.mouse_move(*button_coords["aura_first"], speed=10)
    ahk.click()
    time.sleep(1)

    # Move to the second position and click
    ahk.mouse_move(*button_coords["aura_second"], speed=10)
    ahk.click()
    time.sleep(1)

    # Type the aura name
    pyautogui.write(aura_name)
    time.sleep(1)

    # Move to the third position and click
    ahk.mouse_move(*button_coords["aura_third"], speed=10)
    ahk.click()
    time.sleep(1)

    # Move to the fourth position and click
    ahk.mouse_move(*button_coords["aura_fourth"], speed=10)
    ahk.click()
    time.sleep(1)

    # Move back to the first position and click again to finalize
    ahk.mouse_move(*button_coords["aura_first"], speed=10)
    ahk.click()
    time.sleep(1)

    # Take a screenshot with success message
    filename = take_screenshot(f"equipped_{aura_name}.png")

    if filename is None:
        await ctx.respond("Roblox is not open or not in focus. Please open Roblox in windowed mode.")
        return

    # Send the screenshot to the user with success message
    await ctx.respond(file=discord.File(filename), content=f"Successfully Equipped {aura_name}")

    # Clean up the file after sending
    os.remove(filename)

# Bot ready event
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')

# Run the bot
asyncio.run(run_bot())
