import pygetwindow as gw
import pyautogui
import time

def pop_up_terminal():
    terminal = gw.getActiveWindow()
    terminal.activate(
        
    )
def locate_tab(browser_name, tabname_target):

    terminal = gw.getActiveWindow()

    found = False

    for browser in gw.getAllWindows():

        if browser_name.lower() not in browser.title.lower():
            continue

        if not browser.title.strip():
            continue

        browser.activate()

        time.sleep(1)


        first_tab = ""
        started = False

        for i in range(50):

            current = gw.getActiveWindow()

            if not current:
                continue

            title = current.title.strip()

            if not title:
                continue


            if not started:
                first_tab = title
                started = True

            elif title == first_tab:
                break

            for target in tabname_target:

                if target.lower() in title.lower():


                    found = True
                    break

            if found:
                break

            # Opera / Opera GX fix
            if "opera" in browser_name.lower():

                pyautogui.hotkey("ctrl", "pagedown")

            else:

                pyautogui.hotkey("ctrl", "tab")

            time.sleep(0.5)

        if found:
            break

    if not found and terminal:

        return False