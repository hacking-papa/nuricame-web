#!/usr/bin/env python3
from typing import Any, Union

import cv2 as cv

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
        self.net = cv.dnn.readNetFromCaffe("deploy.prototxt", "hed_pretrained_bsds.caffemodel")

    def convert(self, image):
        cv.dnn_registerLayer("Crop", CropLayer)
        scale: Union[float, Any] = max(A4_WIDTH / image.shape[1], A4_HEIGHT / image.shape[0])
        self.image = cv.resize(image, dsize=None, fx=scale, fy=scale, interpolation=cv.INTER_CUBIC)


if __name__ == "__main__":
    hed = HED()
