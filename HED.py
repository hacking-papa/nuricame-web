#!/usr/bin/env python3

""" Holistically-Nested Edge Detection """

import cv2

A4_WIDTH: int = 2894
A4_HEIGHT: int = 4092
PROCESSING_RESOLUTION: int = 512


class CropLayer:
    def __init__(self, params, blobs):
        self.start_x = 0
        self.end_x = 0
        self.start_y = 0
        self.end_y = 0

    def getMemoryShapes(self, inputs):
        input_shape, target_shape = inputs[0], inputs[1]
        batch_size, num_channels = input_shape[0], input_shape[1]
        height, width = target_shape[2], target_shape[3]

        self.start_x = int((input_shape[3] - target_shape[3]) / 2)
        self.start_y = int((input_shape[2] - target_shape[2]) / 2)
        self.end_x = self.start_x + width
        self.end_y = self.start_y + height

        return [[batch_size, num_channels, height, width]]

    def forward(self, inputs):
        return [inputs[0][:, :, self.start_y:self.end_y, self.start_x:self.end_x]]


def convert(image):
    cv2.dnn_registerLayer("Crop", CropLayer)
    net = cv2.dnn.readNetFromCaffe("deploy.prototxt", "hed_pretrained_bsds.caffemodel")
    blob = cv2.dnn.blobFromImage(image, scalefactor=1.0, size=(PROCESSING_RESOLUTION, PROCESSING_RESOLUTION),
                                 mean=(104.00698793, 116.66876762, 122.67891434), swapRB=False, crop=True)
    net.setInput(blob)
    hed = net.forward()
    hed = cv2.resize(hed[0, 0], (A4_WIDTH, A4_WIDTH), interpolation=cv2.INTER_LINEAR_EXACT)
    hed = (255 * hed).astype("uint8")
    output = cv2.bitwise_not(hed)
    print(f"Output Type: {type(output)}")  # TODO: for Debug!
    print(f"Output Shape: {output.shape}")  # TODO: for Debug!
    cv2.dnn_unregisterLayer("Crop")
    return output


if __name__ == "__main__":
    from pathlib import Path
    import main

    sample_dir = Path("./sample")
    output_dir = Path("./sample/output")

    for sample_img in (x for x in sample_dir.glob("*") if main.allowed_file(x.name)):
        print(f"Converting: {sample_img}")
        img = cv2.imread(str(sample_img))
        cv2.imwrite(str(output_dir / sample_img.name), convert(img))
