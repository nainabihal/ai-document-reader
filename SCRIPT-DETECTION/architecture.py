import cv2
import numpy as np
from paddleocr import PaddleOCR

# ---- Text detector (language-agnostic) ----
detector = PaddleOCR(
    det=True,
    rec=False,
    cls=False,
    show_log=False
)

# ---- Language-specific recognizers ----
ocr_en = PaddleOCR(lang="en", det=False, cls=False, show_log=False)
ocr_hi = PaddleOCR(lang="hi", det=False, cls=False, show_log=False)
ocr_ta = PaddleOCR(lang="ta", det=False, cls=False, show_log=False)

REC_MAP = {
    "en": ocr_en,
    "hi": ocr_hi,
    "ta": ocr_ta
}

# ---- Line Cropping Utility (Critical) ----
def crop_line(image, box):
    pts = np.array(box).astype(int)
    x, y, w, h = cv2.boundingRect(pts)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY).astype("uint8")
    return image[y:y+h, x:x+w]

# ---- Script Detection (Unicode-based, Fast & Reliable) ----
def detect_script(text):
    for ch in text:
        code = ord(ch)
        if 0x0900 <= code <= 0x097F:
            return "hi"   # Devanagari
        if 0x0B80 <= code <= 0x0BFF:
            return "ta"   # Tamil
    return "en"

# ---- Line Recognition with Routing (Core Logic) ----
def recognize_line(line_img):
    result_en = None
    result_hi = None

    try:
        result_en = ocr_en.ocr(line_img, det=False, cls=False)
        result_hi = ocr_hi.ocr(line_img, det=False, cls=False)
    except Exception:
        return {
            "text": "",
            "confidence": 0.0,
            "script": "en"
        }

    if not result_en or not result_en[0] or not result_hi or not result_hi[0]:
        return {
            "text": "",
            "confidence": 0.0,
            "script": "en"
        }

    payload = result_en[0][0],result_hi[0][0]

    text=""
    confidence=0
    for out in payload:
        if out[0] is not None:
            text, conf = out
            if conf > confidence:
                text = text
                confidence = conf

    # ---- Handle PaddleOCR output variants ----
    # if isinstance(payload, tuple):
    #     text, confidence = payload
    # elif isinstance(payload, float):
    #     text = ""
    #     confidence = payload
    # else:
    #     text = ""
    #     confidence = 0.0

    # script = detect_script(text)

    # recognizer = REC_MAP.get(script, ocr_en)
    # final = recognizer.ocr(line_img, det=False, cls=False)

    # if not final or not final[0]:
    #     return {
    #         "text": "",
    #         "confidence": float(confidence),
    #         "script": script
    #     }

    # final_payload = final[0][0]

    # if isinstance(final_payload, tuple):
    #     final_text, final_conf = final_payload
    # elif isinstance(final_payload, float):
    #     final_text = ""
    #     final_conf = final_payload
    # else:
    #     final_text = ""
    #     final_conf = 0.0

    # return {
    #     "text": final_text,
    #     "confidence": float(final_conf),
    #     "script": script
    # }
    return {
        "text": text,
        "confidence": float(confidence)
    }


# ---- Full Document OCR Pipeline ----
def ocr_document(image_path):
    image = cv2.imread(image_path)
    assert image is not None, "Image not found"

    det_result = detector.ocr(image, cls=False)

    output = []

    for line in det_result[0]:
        box = line[0]
        line_img = crop_line(image, box)

        rec = recognize_line(line_img)

        output.append({
            "bbox": box,
            "text": rec["text"],
            # "script": rec["script"],
            "confidence": rec["confidence"]
        })

    return output

result = ocr_document("172448470_3_pg15.png")

for line in result:
    print(
        # f"[{line['script']}] "
        f"{line['text']} "
        f"(conf={line['confidence']:.2f})"
    )

# print(result)