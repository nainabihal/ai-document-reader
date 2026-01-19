import cv2
from paddleocr import PaddleOCR

# ✅ Angle classifier enabled here
ocr = PaddleOCR(
    use_angle_cls=True,
    lang="hi"  # Changed to Hindi for better Hindi text detection
)

def run_ocr(image_path):
    image = cv2.imread(image_path)
    if image is None:
        return []

    # ❌ DO NOT pass cls=True here
    result = ocr.ocr(image)

    ocr_data = []

    for page in result:
        for box, (text, conf) in page:
            ocr_data.append({
                "text": text.strip(),
                "confidence": float(conf),
                "bbox": box
            })

    return ocr_data
