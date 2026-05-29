from libs import *
import time

class Main:
    def __init__(self):
        pass

if __name__ == "__main__":
    image_index = actual_file_index(files_path="imgs")
    time.sleep(1)
    data = get_data()
    locate_tab("chrome",["catho","vaga"])
    fullscreen_tab()
    capture_screenshot(image_index,data)
    image_treatmeant(image_index,data)
    text = get_last_text()
    job = parse_job(text)
    path = save_job(job)
    if locate_and_click(image_index,data,"Pular") == False:
        pyautogui.hotkey("f5")
        locate_and_click(image_index,data,"Pular")