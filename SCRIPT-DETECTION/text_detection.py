from paddleocr import PaddleOCR
import cv2
import numpy as np

detector = PaddleOCR(
    det=True,
    rec=False,
    cls=False,
    show_log=False
)
det_result = detector.ocr("172589759_3_pg6.png") 


if __name__ == "__main__":
    print((det_result[0][0][1][0]))