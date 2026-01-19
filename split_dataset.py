import os
import random
import shutil
from pathlib import Path

SOURCE_DIR = "train (1)/train"  # folder with all PNGs
DEST_DIR = "dataset/images"

TRAIN_RATIO = 0.7
VAL_RATIO = 0.15
TEST_RATIO = 0.15

random.seed(42)

def split_images():
    images = list(Path(SOURCE_DIR).glob("*.png"))
    random.shuffle(images)

    total = len(images)
    train_end = int(total * TRAIN_RATIO)
    val_end = train_end + int(total * VAL_RATIO)

    splits = {
        "train": images[:train_end],
        "val": images[train_end:val_end],
        "test": images[val_end:]
    }

    for split, files in splits.items():
        split_dir = Path(DEST_DIR) / split
        split_dir.mkdir(parents=True, exist_ok=True)

        for file in files:
            shutil.copy(file, split_dir / file.name)

    print("✅ Dataset split completed")
    print(f"Train: {len(splits['train'])}")
    print(f"Val: {len(splits['val'])}")
    print(f"Test: {len(splits['test'])}")

if __name__ == "__main__":
    split_images()
