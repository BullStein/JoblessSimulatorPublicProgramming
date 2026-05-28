import json
import os

data_dir = "data/data.json"

base_data = {
    "tesseract": {
        "image_index": 0,
        "text_index": 0,
        "lang": "por"
    }
}

def check_path_existence(path):
    dir_path = os.path.dirname(path)
    if dir_path:
        os.makedirs(dir_path, exist_ok=True)
    
    if not os.path.exists(path) and path == "data/data.json":
        with open(path, "w", encoding="utf-8") as f:
            json.dump(base_data, f, indent=4)
    
def ensure_file(path):
    dir_path = os.path.dirname(path)
    if dir_path:
        os.makedirs(dir_path, exist_ok=True)
    
    if not os.path.exists(path) and path == "data/data.json":
        with open(path, "w", encoding="utf-8") as f:
            json.dump(base_data, f, indent=4)

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def get_data(data_path=data_dir):
    check_path_existence(data_path)

    try:
        with open(data_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        with open(data_path, "w", encoding="utf-8") as f:
            json.dump(base_data, f, indent=4)
        return base_data

def actual_file_index(data=None, files_path="imgs"):
    ensure_dir(files_path)

    if data is None:
        data = get_data()

    file_list = [
        f for f in os.listdir(files_path)
        if os.path.isfile(os.path.join(files_path, f))
    ]
    
    file_qnty = len(file_list)
    
    numbers = []
    for filename in file_list:
        number_str = ""
        for char in filename:
            try:
                int(char)
                number_str += char
            except (ValueError, TypeError):
                if number_str:
                    numbers.append(int(number_str))
                    number_str = ""
        if number_str:
            numbers.append(int(number_str))
    
    if numbers:
        last_filename_index = max(numbers) + 1
    else:
        last_filename_index = 0
    
    if (
        "tesseract" in data and
        "image_index" in data["tesseract"] and
        file_qnty == data["tesseract"]["image_index"]
    ):
        return data["tesseract"]["image_index"]
    if last_filename_index < file_qnty:
        return file_qnty
    else:
        return last_filename_index

def actual_text_index(data=None, texts_path="texts"):
    ensure_dir(texts_path)

    if data is None:
        data = get_data()

    file_list = [
        f for f in os.listdir(texts_path)
        if os.path.isfile(os.path.join(texts_path, f))
    ]

    file_qnty = len(file_list)

    if (
        "tesseract" in data and
        "text_index" in data["tesseract"] and
        file_qnty == data["tesseract"]["text_index"]
    ):
        return data["tesseract"]["text_index"]

    return file_qnty

def save_data(new_data, data_path=data_dir):
    directory = os.path.dirname(data_path)

    if directory:
        os.makedirs(directory, exist_ok=True)

    with open(data_path, "w", encoding="utf-8") as f:
        json.dump(new_data, f, indent=4)