# Radiance Actions © 2024 by Radiant Team is licensed under Creative Commons Attribution-ShareAlike 4.0 International

actionlib.tap_ui_navigation()
for i in range(4):
    sleep(0.1)
    kc.tap(Key.left) 
for i in range(5 - button_num):
    sleep(0.1)
    kc.tap(Key.up)
sleep(0.1)
kc.tap(Key.enter)
actionlib.tap_ui_navigation()
