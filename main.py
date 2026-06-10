from libs import *
import time


class App:
    def __init__(self):
        self.data = get_data()
        self.image_index = actual_file_index(files_path="imgs")
        self.run_process()

    # ── Core flow ──────────────────────────────────────────────────────────────

    def run_process(self) -> None:
        self.locate_job_tab()
        self.pre_processing()
        fullscreen_tab()
        capture_screenshot(self.image_index, self.data)
        image_treatment(self.image_index, self.data)
        reset_zoom()
        set_zoom(150)
        capture_screenshot(self.image_index, self.data)
        self.skip_vacancy_suggest()
        reset_zoom()

    # ── Navigation ─────────────────────────────────────────────────────────────

    def locate_job_tab(self) -> None:
        try:
            found = locate_tab("chrome", ["catho", "vaga"])
            if not found:
                set_zoom(100)
                open_new_catho_tab()
                time.sleep(2)
        except Exception:
            pass  # TODO: handle or log failure to locate/open tab

    def correct_tab(self) -> None:
        if get_url_active_tab() != "https://www.catho.com.br/vagas/sugestao":
            pass  # TODO: redirect or switch to the correct tab

    # ── Auth / pre-processing ──────────────────────────────────────────────────

    def pre_processing(self) -> None:
        while not self._is_logged():
            pop_up_terminal()
            input("Entre com a sua conta para continuar...\npressione qualquer tecla para continuar >> ")

    def _is_logged(self) -> bool:
        return get_url_active_tab() != "catho.com.br/signin/"

    # ── Actions ────────────────────────────────────────────────────────────────

    def skip_vacancy_suggest(self) -> None:
        locate_and_click(self.image_index, self.data, "Pular")

    def close_ad(self) -> bool:
        return locate_and_click(self.image_index, self.data, ["Agora não"])


if __name__ == "__main__":  
    app = App()