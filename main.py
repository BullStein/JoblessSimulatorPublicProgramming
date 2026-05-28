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
    time.sleep(1)
    capture_screenshot(image_index,data)
    print(image_treatmeant(image_index,data))
    time.sleep(1)
    locate_and_click(image_index,data,"Pular")