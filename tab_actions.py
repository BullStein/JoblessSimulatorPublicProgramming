import pygetwindow as gw
import pyautogui

def fullscreen_tab():
  

    window = gw.getActiveWindow()

    screen_width, screen_height = pyautogui.size()

    if window.width >= screen_width and window.height >= screen_height:
        pass
    else:
        pyautogui.hotkey("f11")

def scroll_page_down():
    pyautogui.scroll(-500)