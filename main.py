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
        time.sleep(7)
        self._save_logged_instance()
        self.main_loop()

    # ── Navigation ─────────────────────────────────────────────────────────────

    def locate_job_tab(self) -> None:
        try:
            found = locate_tab("chrome", ["catho", "vaga", "Currículo"])
            if not found:
                open_new_catho_acount_tab()
                notificate("Notificação", "Catho não encontrada abrindo Nova Aba e login atual.")
                time.sleep(2)
            else:
                notificate("Notificação", "Aba encontrada, redirecionando para checar login atual.")
                redirect_actual_tab("https://www.catho.com.br/curriculo/dados-pessoais/")
        except Exception:
            pass  # TODO: handle or log failure to locate/open tab
        time.sleep(3)

    def correct_tab(self) -> None:
        if get_url_active_tab() != "https://www.catho.com.br/vagas/sugestao":
            pass  # TODO: redirect or switch to the correct tab

    # ── Auth / pre-processing ──────────────────────────────────────────────────

    def pre_processing(self) -> None:
        not_logged_index = 0
        while not self._is_logged():
            notificate_and_wait(
                "Alerta!",
                "Não foi possível acessar a conta. Por favor, realize o login e, em seguida, pressione Enter no terminal para continuar."
            )
            locate_tab("chrome", ["catho","vaga"])
            redirect_actual_tab("https://www.catho.com.br/curriculo/dados-pessoais/")
            time.sleep(2)

        notificate("Notificação","Aba e conta encontrada, prosseguindo com a instância atual")
        locate_tab("chrome", ["catho","vaga"])
        redirect_actual_tab("https://www.catho.com.br/vagas/sugestao/")
        fullscreen_tab()

    def _is_logged(self) -> bool:
        possible_redirect_urls = ["catho.com.br/signin/","https://www.catho.com.br/"]
        return get_url_active_tab() not in possible_redirect_urls

    def _save_logged_instance(self) -> None:
        new_data = get_data()
        new_data["account"]["is_logged"] = True
        save_data(new_data)

    # ── Actions ────────────────────────────────────────────────────────────────

    def skip_vacancy_suggest(self) -> None:
        locate_and_click(self.image_index, self.data, "Pular")

    def close_ad(self) -> bool:
        return locate_and_click(self.image_index, self.data, ["Agora não"])

    def take_image_treatmeant(self) -> None:
        set_zoom(67)
        scroll(-120)
        time.sleep(1.5)
        capture_screenshot(self.image_index, self.data)
        image_treatmeant(self.image_index, self.data)
        reset_zoom()
        scroll_page_up()
    
    def find_buttons(self) -> None:
        scroll_page_up()
        capture_screenshot(self.image_index, self.data)
        image_treatmeant(self.image_index, self.data)

    # ── Main Loop ──────────────────────────────────────────────────────────────
    
    def main_loop(self) -> None:
        self.take_image_treatmeant()
        text = get_last_text()
        job = parse_job(text)
        path = save_job_parsed(job)
        data = get_data()
        locate_and_click(data=data,target_text="Quero me candidatar")
if __name__ == "__main__":
    app = App()
    # except KeyboardInterrupt:
    #     print("\n[Encerrado pelo usuário]")
    #     input("pressione qualquer tecla para encerrar \n>>")