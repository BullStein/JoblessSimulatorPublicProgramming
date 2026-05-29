from PIL import Image
import pytesseract
import getpass
import pyautogui
import cv2
import numpy as np


def locate_and_click(image_index, data, target_text):

    image_path = f"imgs/screenshot_{image_index}.png"

    pc_name = getpass.getuser()

    tesseract_lang_pack = data["tesseract"]["lang"]

    pytesseract.pytesseract.tesseract_cmd = (
        rf"C:\Users\{pc_name}\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
    )

    image = Image.open(image_path)

    img = np.array(image)

    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    gray = cv2.GaussianBlur(
        gray,
        (3, 3),
        0
    )

    gray = cv2.threshold(
        gray,
        200,
        255,
        cv2.THRESH_BINARY_INV
    )[1]

    ocr_data = pytesseract.image_to_data(
        gray,
        lang=tesseract_lang_pack,
        output_type=pytesseract.Output.DICT
    )

    for i in range(len(ocr_data["text"])):

        detected_text = ocr_data["text"][i].strip()

        if not detected_text:
            continue

        if target_text.lower() in detected_text.lower():

            x = ocr_data["left"][i]
            y = ocr_data["top"][i]
            w = ocr_data["width"][i]
            h = ocr_data["height"][i]

            center_x = x + w // 2
            center_y = y + h // 2

            print(f"Found: {detected_text}")
            print(f"Position: {center_x}, {center_y}")

            pyautogui.moveTo(
                center_x,
                center_y,
                duration=0
            )

            pyautogui.click()

            return True

    return False