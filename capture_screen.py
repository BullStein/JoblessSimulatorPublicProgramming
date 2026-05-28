import pyautogui
import os
from data_manage import *

def capture_screenshot(image_index, data):
    dir = "imgs"
    os.makedirs(dir, exist_ok=True)
    
    image_path = os.path.join(dir, f"screenshot_{image_index}.png")

    imagem = pyautogui.screenshot()
    imagem.save(image_path)

    data["tesseract"]["image_index"] = image_index + 1

    save_data(data)

if __name__ == "__main__":
    data = get_data(data_dir)

    if data:
        index = actual_file_index(files_path="imgs")
        capture_screenshot(index, data)
    else:
        print("Erro ao carregar dados")