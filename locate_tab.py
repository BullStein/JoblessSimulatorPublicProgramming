import pygetwindow as gw
import pyautogui
import time


def locate_tab(browser_name, tabname_target):

    terminal = gw.getActiveWindow()

    found = False

    max_tabs = 0

    # count browser windows
    for window in gw.getAllWindows():

        if browser_name.lower() in window.title.lower():

            max_tabs += 1

    max_tabs = max_tabs * 20

    print(f"MAX TABS: {max_tabs}")

    for browser in gw.getAllWindows():

        if browser_name.lower() not in browser.title.lower():
            continue

        if not browser.title.strip():
            continue

        browser.activate()

        time.sleep(1)

        print("\nTESTING WINDOW:")
        print(browser.title)

        visited_tabs = []

        for i in range(max_tabs):

            current = gw.getActiveWindow()

            if not current:
                continue

            title = current.title

            if not title.strip():
                continue

            if title in visited_tabs:
                break

            visited_tabs.append(title)

            print(f"[{i}] {title}")

            # checks all target names
            for target in tabname_target:

                if target.lower() in title.lower():

                    print(f"\nFOUND: {target}")

                    found = True

                    break

            if found:
                break

            pyautogui.hotkey("ctrl", "tab")

            time.sleep(0.7)

        if found:
            break

    if not found and terminal:

        terminal.activate()