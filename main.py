from libs import *
import time

class Main:
    def __init__(self):
        self.data = self.__get_data()
        self.image_index = 
    def run_process(data,image_index,):

    def __get_data(self):
        data = get_data()
        return data
    def image_index(self):
        image_index = actual_file_index(files_path="imgs")
        return image_index
    def locate_job_tab(self):
        if not locate_tab("chrome",["catho","vaga"]):
            break
        set_zoom(150)
    def capture_screenshot(self,image_index,data)
        capture_screenshot(image_index,data)
        
if __name__ == "__main__":
    image_index = actual_file_index(files_path="imgs")
    data = get_data()
    fullscreen_tab()
    reset_zoom()
    set_zoom(150)
    capture_screenshot(image_index,data)
    locate_and_click(image_index,data,"Pular")
    reset_zoom()
    # image_treatmeant(image_index,data)
    # text = get_last_text()
    # job = parse_job(text)
    # job_index = last_job_index()
    # path = save_job(job, index=job_index)
    # if not locate_and_click(image_index,data,"Pular"):
    #     pyautogui.hotkey("f5")
    #     image_index = actual_file_index(files_path="imgs")
    #     capture_screenshot(image_index,data)
    #     image_treatmeant(image_index,data)
    #     locate_and_click(image_index,data,"Pular")
    #     print("botão não encontrado")