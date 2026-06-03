import pygetwindow as gw
import pyautogui

def fullscreen_tab():
    window = gw.getActiveWindow()

    if window is None:
        return

    screen_width, screen_height = pyautogui.size()

    if window.width < screen_width or window.height < screen_height:
        pyautogui.press("f11")

ZOOM_LIST = [25, 33, 50, 67, 75, 80, 90, 100, 110, 125, 150, 175, 200, 250, 300, 400, 500]

def set_zoom(level: int = 100) -> None:
    reset_zoom()
    target_index = ZOOM_LIST.index(level)
    default_index = ZOOM_LIST.index(100)
    steps = abs(target_index - default_index)

    for _ in range(steps):
        if target_index > default_index:
            pyautogui.hotkey("ctrl", "+")
        else:
            pyautogui.hotkey("ctrl", "-")

def reset_zoom() -> None:
    pyautogui.hotkey("ctrl", "0")

def scroll_page_down() -> None:
    pyautogui.scroll(-500)
    
def scroll_page_up() -> None:
    pyautogui.scrool(500)