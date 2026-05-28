from libs import *
import time

if __name__ == "__main__":
    image_index = actual_file_index(files_path="imgs")
    time.sleep(5)
    data = get_data()
    capture_screenshot(image_index,data)
    print(image_treatmeant(image_index,data))