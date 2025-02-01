resolution_settings = config.read_resolution()

def detect_ui_nav(bbox):
    px = ImageGrab.grab(bbox).load()
    for x in range(0, bbox[2] - bbox[0]):
        for y in range(0, bbox[3] - bbox[1]):
            if px[x, y] == (255, 255, 255):
                return True
    return False

# Pick Potion
for i in range(3):
    tap_ui_navigation()
tap(Key.left)

for i in range(11):
    tap(Key.down)

for i in range(2):
    tap_ui_navigation()    

index = int(config.config_data["potion_crafting"]["options"][potion_name]["index"])

for i in range(index-1):
    tap(Key.down)
tap(Key.enter)  

# Get to crafting menu
for i in range(4):
    tap_ui_navigation()

for i in range(2):
    tap(Key.left)

# Align the options
for i in range(5):
    tap(Key.down)

for i in range(5):
    tap(Key.up)

# Get to crafting menu
for i in range(4):
    tap_ui_navigation()

for i in range(2):
    tap(Key.left)
tap(Key.down)

# Start Crafting
restart = True
while restart == True:
    restart = False
    for i in range(len(config.config_data["potion_crafting"]["options"][potion_name]["ingredients"])):
        max_input = int(config.config_data["potion_crafting"]["options"][potion_name]["max_ingredient"])
        while True:
            tap(Key.enter)

            for i in range(4):
                kc.tap(Key.backspace)
                tap_sleep(True)
            
            for i in str(int(max_input)):
                kc.press(str(i))
                tap_sleep(True)
                kc.release(str(i))
                tap_sleep(True)
                
            tap(Key.enter)
            tap(Key.right)
            tap(Key.enter)
            
            if detect_ui_nav([eval(i) for i in resolution_settings["potion_crafting"]["leaderboard_close_button"].split(",")]) == True:
                for i in range(2):
                    tap(Key.left)
                restart = True
                break
            else:
                tap(Key.left)

                if max_input == 1:
                    break
                max_input = -(max_input // -2.0)
        tap(Key.down)
        
        if detect_ui_nav([eval(i) for i in resolution_settings["potion_crafting"]["autoroll_button"].split(",")]) == True: # Recorded in 1920x1080 100%
            break
        if restart == True:
            break
    
tap_ui_navigation()
