def calculate_confidence(extracted_fields, ocr_data):
    text_fields = ["dealer_name", "model_name", "horse_power", "asset_cost"]

    present_text = sum(
        1 for f in text_fields if extracted_fields.get(f)
    )

    visual_fields = ["signature", "stamp"]
    present_visual = sum(
        1 for f in visual_fields
        if extracted_fields.get(f, {}).get("present")
    )

    avg_ocr_conf = (
        sum(x["confidence"] for x in ocr_data) / len(ocr_data)
        if ocr_data else 0
    )

    coverage_score = (present_text + present_visual) / 6
    confidence = 0.6 * coverage_score + 0.4 * avg_ocr_conf

    return round(min(confidence, 0.99), 2)
