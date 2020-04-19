#!/usr/bin/env python3

""" Morphology Dilation and Erosion """

import cv2
import numpy as np

img = cv2.imread("sample/output/01_2400x3200.jpg", 0)

ret, img = cv2.threshold(img, 127, 255, cv2.THRESH_OTSU)
print(f"Threshold: {ret}")
cv2.imwrite("sample/output/threshold.jpg", img)

size = np.size(img)
skelton = np.zeros(img.shape, np.uint8)

element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))

while True:
    open = cv2.morphologyEx(img, cv2.MORPH_OPEN, element)
    temp = cv2.subtract(img, open)
    eroded = cv2.erode(img, element)
    skelton = cv2.bitwise_or(skelton, temp)
    img = eroded.copy()
    if cv2.countNonZero(img) == 0:
        break

cv2.imwrite("sample/output/skelton.jpg", cv2.bitwise_not(skelton))
