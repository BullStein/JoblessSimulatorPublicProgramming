from libs import *
import time

class App:
    def __init__(self):
        self.data = self.__get_data()
        self.image_index = self.__get_image_index()
        self.run_process()  

    def run_process(self) -> None:
        self.locate_job_tab()
        self.capture_screenshot()
        self.treat_image(self.image_index, self.data)
        reset_zoom()
        set_zoom(150)
        self.capture_screenshot()
        self.skip_vacancy_sugest()
        reset_zoom()

    def treat_image(self, image_index, data) -> None:
        image_treatmeant(image_index, data)

    def skip_vacancy_sugest(self) -> None:
        locate_and_click(self.image_index, self.data, "Pular")

    def close_ad(self) -> bool:
        return locate_and_click(self.image_index, self.data, ["Agora não"])

    def __get_data(self) -> dict:
        return get_data()

    def __get_image_index(self) -> int:
        return actual_file_index(files_path="imgs")

    def fullscreen_tab(self) -> None:
        fullscreen_tab()

    def is_logged(self) -> bool:
        return "https://www.catho.com.br/signin/" == get_url_active_tab()
    
    def pre_processing():
        while not self.is_logged():
            pop_up_terminal()
            print("Entre com a sua conta para continuar...\npressione qualquer tecla para continuar >>")
    
    def locate_job_tab(self):
        found = locate_tab("chrome", ["catho", "vaga"])
        if found == False:
            open_new_catho_tab()
            time.sleep(2)
        self.fullscreen_tab()
        set_zoom(75)

    def capture_screenshot(self) -> None: 
        capture_screenshot(self.image_index, self.data)


if __name__ == "__main__":
    app = App()