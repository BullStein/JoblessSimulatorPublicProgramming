from PIL import Image
import pytesseract
import getpass
from text_treatmeant import *

def image_treatmeant(image_index,data):
    image_path = f"imgs/screenshot_{image_index}.png" 
    pc_name = getpass.getuser()
    tesseract_lang_pack = data["tesseract"]["lang"]
    try:
        pytesseract.pytesseract.tesseract_cmd = r"C:\Users\{}\AppData\Local\Programs\Tesseract-OCR\tesseract.exe".format(pc_name)
    except Exception:
        print("github : https://github.com/tesseract-ocr/tesseract\nlanguage package: ")
    #sometimes i fell like my life was in vain, in both ways, if not in all ways.    
    text = pytesseract.image_to_string(image_path,lang=tesseract_lang_pack)
    
    try:
        save_text(text)
    except Exception:
        return print("Erro ao salvar texto")
