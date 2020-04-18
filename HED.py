#!/usr/bin/env python3
from typing import Any, Union

import cv2

A4_WIDTH: int = 2894
A4_HEIGHT: int = 4092


class CropLayer:
    def __init__(self, params, blobs):
        self.x_start = 0
        self.x_end = 0
        self.y_start = 0
        self.y_end = 0

    def getMemoryShapes(self, inputs):
        input_shape, target_shape = inputs[0], inputs[1]
        batch_size, num_channels = input_shape[0], input_shape[1]
        height, width = target_shape[2], target_shape[3]

        self.y_start = int((input_shape[2] - target_shape[2]) / 2)
        self.x_start = int((input_shape[3] - target_shape[3]) / 2)
        self.y_end = self.y_start + height
        self.x_end = self.x_start + width

        return [[batch_size, num_channels, height, width]]

    def forward(self, inputs):
        return [inputs[0][:, :, self.y_start:self.y_end, self.x_start:self.x_end]]


class HED:
    def __init__(self, logger=None):
        if not logger:
            import logging
            self.logger = logging.getLogger(__name__)
            self.logger.setLevel(logging.DEBUG)
        self.image = None
        self.output = None
        self.net = cv2.dnn.readNetFromCaffe("deploy.prototxt", "hed_pretrained_bsds.caffemodel")
        cv2.dnn_registerLayer("Crop", CropLayer)

    def convert(self, image):
        scale: Union[float, Any] = max(A4_WIDTH / image.shape[1], A4_WIDTH / image.shape[0])
        self.image = cv2.resize(image, dsize=None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
        self.output = self.image
        return self.output


if __name__ == "__main__":
    from pathlib import Path
    import main

    sample_dir = Path("./sample")
    output_dir = Path("./sample/output")

    hed = HED()

    for sample_img in (x for x in sample_dir.glob("*") if main.allowed_file(x.name)):
        print(f"Converting: {sample_img}")
        cv2.imwrite(str(output_dir / sample_img.name), hed.convert(cv2.imread(str(sample_img))))
