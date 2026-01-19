import re

def extract_fields(ocr_data):
    fields = {
        "dealer_name": None,
        "model_name": None,
        "horse_power": None,
        "asset_cost": None,
        "signature": {"present": False},
        "stamp": {"present": False}
    }

    full_text = " ".join(x["text"] for x in ocr_data)

    for i, t in enumerate(ocr_data):
        txt = t["text"].lower()

        if "dealer" in txt and i + 1 < len(ocr_data):
            fields["dealer_name"] = ocr_data[i + 1]["text"]

        if "tractor" in txt:
            fields["model_name"] = t["text"]

        hp = re.search(r"(\d{2,3})\s*(hp|bhp)", txt)
        if hp:
            fields["horse_power"] = int(hp.group(1))

        amt = re.search(r"\d{1,2},\d{2},\d{3}", t["text"])
        if amt:
            fields["asset_cost"] = int(amt.group().replace(",", ""))

    return fields
