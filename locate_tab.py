import pygetwindow as gw
import pyautogui
import time


def locate_tab(browser_name: str, tabname_target: list[str]) -> bool:
    terminal = gw.getActiveWindow()
    found = False

    for browser in gw.getAllWindows():
        if browser_name.lower() not in browser.title.lower():
            continue
        if not browser.title.strip():
            continue

        browser.activate()
        time.sleep(1)

        first_tab = None

        for i in range(50):
            current = gw.getActiveWindow()
            if not current:
                continue

            title = current.title.strip()
            if not title:
                continue


            # Check targets FIRST, before comparing to first_tab
            for target in tabname_target:
                if target.lower() in title.lower():
                    found = True
                    break

            if found:
                break

            # Now check if we've looped back to the start
            if first_tab is None:
                first_tab = title
            elif title == first_tab:
                break  # Full loop complete, target not found

            # Advance to next tab
            if "opera" in browser_name.lower():
                pyautogui.hotkey("ctrl", "pagedown")
            else:
                pyautogui.hotkey("ctrl", "tab")

            time.sleep(0.5)

        if found:
            break

    if not found and terminal:
        return found
    return found