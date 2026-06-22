from PIL import Image
import pytesseract
import getpass
import pyautogui
import cv2
import numpy as np

""" 
    funções privadas não devem ser usadas fora da função principal ou derivadas
    _get_tesseract_cmd : pega o caminho do úsuario 
    _preprocess: pre-processa a imagem com filtos para exclarecer os botões e seus textos
    _run_ocr : roda o ocr com suas configurações
    _search_text: percorre o ocr no texto
    locate_and_click : usa todas as funções privadas para achar o texto/botão e interargir
"""


def _get_tesseract_cmd() -> str:
    user = getpass.getuser()
    return rf"C:\Users\{user}\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"


def _preprocess(img_bgr: np.ndarray) -> list[np.ndarray]:
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    versions = []

    versions.append(gray)

    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    versions.append(clahe.apply(gray))

    adaptive = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 11, 2
    )
    versions.append(adaptive)
    versions.append(cv2.bitwise_not(adaptive))

    return versions


def _run_ocr(image: np.ndarray, lang: str) -> dict:
    config = "--psm 11 --oem 3"
    return pytesseract.image_to_data(
        image,
        lang=lang,
        config=config,
        output_type=pytesseract.Output.DICT
    )


def _search_text(ocr_data: dict, target_text: str, tolerance: int = 10) -> list[dict]:
    matches = []
    target_lower = target_text.lower()
    n = len(ocr_data["text"])

    for i in range(n):
        word = ocr_data["text"][i].strip()
        conf = int(ocr_data["conf"][i])

        if not word or conf < tolerance:
            continue

        if target_lower in word.lower():
            matches.append({
                "text": word,
                "x": ocr_data["left"][i] + ocr_data["width"][i] // 2,
                "y": ocr_data["top"][i] + ocr_data["height"][i] // 2,
                "conf": conf,
                "type": "word",
            })

    lines: dict[tuple, list] = {}
    for i in range(n):
        key = (ocr_data["block_num"][i], ocr_data["line_num"][i])
        lines.setdefault(key, []).append(i)

    for indices in lines.values():
        words = [ocr_data["text"][i].strip() for i in indices]
        line_text = " ".join(w for w in words if w)

        if target_lower in line_text.lower():
            xs = [ocr_data["left"][i] for i in indices if ocr_data["text"][i].strip()]
            ys = [ocr_data["top"][i] for i in indices if ocr_data["text"][i].strip()]
            ws = [ocr_data["left"][i] + ocr_data["width"][i] for i in indices if ocr_data["text"][i].strip()]
            hs = [ocr_data["top"][i] + ocr_data["height"][i] for i in indices if ocr_data["text"][i].strip()]

            if not xs:
                continue

            confs = [int(ocr_data["conf"][i]) for i in indices if ocr_data["conf"][i] != "-1"]
            avg_conf = sum(confs) // len(confs) if confs else 0

            matches.append({
                "text": line_text,
                "x": (min(xs) + max(ws)) // 2,
                "y": (min(ys) + max(hs)) // 2,
                "conf": avg_conf,
                "type": "line",
            })

    return matches


def locate_and_click(
    target_text: str | list[str],
    image_index: int = None,
    data: dict = None,
    min_confidence: int = 30,
    click: bool = True,
) -> bool:
    if data is None:
        data = get_data()

    if image_index is None:
        image_index = data["tesseract"]["image_index"] - 1
        print(image_index)

    pytesseract.pytesseract.tesseract_cmd = _get_tesseract_cmd()

    image_path = f"imgs/screenshot_{image_index}.png"
    lang = data["tesseract"]["lang"]

    pil_image = Image.open(image_path)
    img_bgr = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

    versions = _preprocess(img_bgr)

    targets = [target_text] if isinstance(target_text, str) else target_text

    for target in targets:
        all_matches = []
        for version in versions:
            ocr_data = _run_ocr(version, lang)
            matches = _search_text(ocr_data, target, min_confidence)
            all_matches.extend(matches)

        if not all_matches:
            continue

        all_matches.sort(key=lambda m: (m["type"] == "line", m["conf"]), reverse=True)
        best = all_matches[0]

        if click:
            pyautogui.moveTo(best["x"], best["y"], duration=0.2)
            pyautogui.click()

        return True

    return False