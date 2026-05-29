import os
from data_manage import *

def save_text(text,text_path=None):
    if text_path is None:
        text_path = "texts"
        
    ensure_dir(text_path)  
        
    data = get_data()  
    text_index = actual_file_index(files_path="texts")
    
    file_path = os.path.join(text_path, f"text_{text_index}.txt")
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(text)
    
    
    data["tesseract"]["text_index"] = text_index + 1
    save_data(data)
def get_last_text(text_path=None):
    if text_path is None:
        text_path = "texts"
        
    ensure_dir(text_path)  
        
    data = get_data()  
    text_index = actual_file_index(files_path="texts") - 1
    
    file_path = os.path.join(text_path, f"text_{text_index}.txt")

    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    return text
if __name__ == "__main__":
    save_text("test - 19/05/2026")