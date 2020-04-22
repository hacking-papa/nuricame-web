#!/usr/bin/env python3

""" Compose Image and Frame """

from pathlib import Path

import cv2

FRAME_PATH: Path = Path("frame.png")
TARGET_WIDTH: int = 2500


def compose(img):
    frame = cv2.imread(str(FRAME_PATH))
    frame_height, frame_width, *_ = frame.shape
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    img_height, img_width, *_ = img.shape
    if img_height != TARGET_WIDTH or img_width != TARGET_WIDTH:
        img = cv2.resize(img, (TARGET_WIDTH, TARGET_WIDTH), interpolation=cv2.INTER_LINEAR_EXACT)
        img_height, img_width, *_ = img.shape
    target_x = int((frame_width - img_width) / 2)
    target_y = int((frame_height - img_height) / 2)
    frame[target_y:target_y + img_height, target_x:target_x + img_width] = img
    return frame


if __name__ == "__main__":
    sample_dir_path = Path("./sample")
    output_dir_path = sample_dir_path / "output"
    output_dir_path.mkdir(parents=True, exist_ok=True)

    image = cv2.imread("sample/output/01_2400x3200.jpg")
    framed = compose(image)
    cv2.imwrite(str(output_dir_path / "framed.png"), framed)
