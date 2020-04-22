#!/usr/bin/env python3

""" Frame """

from pathlib import Path

import cv2

FRAME_PATH: Path = Path("frame.png")
TARGET_WIDTH: int = 2000
TARGET_X: int =


def compose(img):
    frame = cv2.imread(str(FRAME_PATH))
    frame_height, frame_width, frame_ch = frame.shape
    img_height, img_width, img_ch = img.shape
    if img_height != TARGET_WIDTH or img_width != TARGET_WIDTH:
        img = cv2.resize(img, (TARGET_WIDTH, TARGET_WIDTH), interpolation=cv2.INTER_LINEAR_EXACT)
    return img


output_dir_path = Path("sample/output")

if __name__ == "__main__":
    sample_dir_path = Path("./sample")
    output_dir_path = sample_dir_path / "output"
    output_dir_path.mkdir(parents=True, exist_ok=True)

    image = cv2.imread("sample/output/01_2400x3200.jpg")
    framed = compose(image)
    cv2.imwrite(str(output_dir_path / "framed.png"), framed)
