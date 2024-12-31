# Radiance Actions © 2024 by Radiant Team is licensed under Creative Commons Attribution-ShareAlike 4.0 International

r_pos = window.get_roblox_window_pos()
actionlib.reset()
sleep(0.1)
click_menu_button(2)
sleep(0.1)

actionlib.tap_ui_navigation()
sleep(0.1)
kc.tap(Key.enter)
sleep(0.1)
ahk.mouse_drag(button="R", from_position=[r_pos.x + r_pos.width*0.2, r_pos.y + 44 + r_pos.height*0.05], x=r_pos.x + r_pos.width*0.2, y=r_pos.y + 400 + r_pos.height*0.05, send_mode="Input", speed=2)
sleep(0.1)
for i in range(50):
    ahk.click(button="WU")
    sleep(0.01)
for i in range(15):
    ahk.click(button="WD")
    sleep(0.01)
actionlib.tap_ui_navigation()
