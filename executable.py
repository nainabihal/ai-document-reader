from ocr import run_ocr
from extractor import extract_fields
from confidence import calculate_confidence
import sys
import json

def extract_from_document(image_path):
    ocr_data = run_ocr(image_path)

    extracted_fields = extract_fields(ocr_data)
    confidence = calculate_confidence(extracted_fields, ocr_data)

    return {
        "fields": extracted_fields,
        "confidence_score": confidence
    }

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python executable.py <image_path>")
        sys.exit(1)
    image_path = sys.argv[1]
    result = extract_from_document(image_path)
    print(json.dumps(result, indent=4))
