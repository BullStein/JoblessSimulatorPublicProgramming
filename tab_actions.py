import pygetwindow as gw
import pyautogui
import pyperclip
import time


def fullscreen_tab():
    window = gw.getActiveWindow()
    if window is None:
        return
    screen_width, screen_height = pyautogui.size()
    if window.width < screen_width or window.height < screen_height:
        pyautogui.press("f11")


def exit_fullscreen_tab():
    window = gw.getActiveWindow()
    if window is None:
        return
    screen_width, screen_height = pyautogui.size()
    if window.width >= screen_width and window.height >= screen_height:
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


def get_url_active_tab() -> str:
    try:
        exit_fullscreen_tab()
        pyautogui.hotkey("ctrl", "l")
        time.sleep(0.2)
        pyautogui.hotkey("ctrl", "a")
        pyautogui.hotkey("ctrl", "c")
        time.sleep(0.1)
        pyautogui.press("escape")
        return pyperclip.paste()
    except KeyboardInterrupt:
        pyautogui.press("escape")  # leave address bar in clean state
        raise                       # bubble up — don't swallow it
    except Exception as e:
        pyautogui.press("escape")  # same cleanup for any other error
        print(f"[get_url_active_tab] erro: {e}")
        return ""


def reset_zoom() -> None:
    pyautogui.hotkey("ctrl", "0")


def scroll_page_down() -> None:
    pyautogui.hotkey("End")


def scroll_page_up() -> None:
    pyautogui.hotkey("Home")

def scroll(val) -> None:
    pyautogui.scroll(val)

def close_tab() -> None:
    pyautogui.hotkey("ctrl", "w")

def open_new_catho_jobsug_tab() -> None:
    pyautogui.hotkey("ctrl", "t")
    pyautogui.write("https://www.catho.com.br/vagas/sugestao/")
    pyautogui.press("enter")  # era hotkey("Enter"), que não funciona

def redirect_actual_tab(url) -> None:
    exit_fullscreen_tab()
    pyautogui.hotkey("ctrl", "l")
    pyautogui.write(url)
    pyautogui.hotkey("Enter")

def open_new_catho_acount_tab() -> None:
    pyautogui.hotkey("ctrl", "t")
    time.sleep(1)
    pyautogui.write("https://www.catho.com.br/curriculo/dados-pessoais/")
    pyautogui.press("enter")  # era hotkey("Enter"), que não funciona
