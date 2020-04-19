#!/usr/bin/env python3

""" Zhang-Suen Algorithm """

import cv2
import numpy as np


def init(kpw, kpb):
    kpw.append(np.array([[0., 0., 0.], [0., 1., 1.], [0., 1., 0.]]))
    kpw.append(np.array([[0., 0., 0.], [0., 1., 0.], [1., 1., 0.]]))
    kpw.append(np.array([[0., 0., 0.], [1., 1., 0.], [0., 1., 0.]]))
    kpw.append(np.array([[1., 0., 0.], [1., 1., 0.], [0., 0., 0.]]))
    kpw.append(np.array([[0., 1., 0.], [1., 1., 0.], [0., 0., 0.]]))
    kpw.append(np.array([[0., 1., 1.], [0., 1., 0.], [0., 0., 0.]]))
    kpw.append(np.array([[0., 1., 0.], [0., 1., 1.], [0., 0., 0.]]))
    kpw.append(np.array([[0., 0., 0.], [0., 1., 1.], [0., 0., 1.]]))
    kpb.append(np.array([[1., 1., 0.], [1., 0., 0.], [0., 0., 0.]]))
    kpb.append(np.array([[1., 1., 1.], [0., 0., 0.], [0., 0., 0.]]))
    kpb.append(np.array([[0., 1., 1.], [0., 0., 1.], [0., 0., 0.]]))
    kpb.append(np.array([[0., 0., 1.], [0., 0., 1.], [0., 0., 1.]]))
    kpb.append(np.array([[0., 0., 0.], [0., 0., 1.], [0., 1., 1.]]))
    kpb.append(np.array([[0., 0., 0.], [0., 0., 0.], [1., 1., 1.]]))
    kpb.append(np.array([[0., 0., 0.], [1., 0., 0.], [1., 1., 0.]]))
    kpb.append(np.array([[1., 0., 0.], [1., 0., 0.], [1., 0., 0.]]))


if __name__ == "__main__":
    kpw = []
    kpb = []
    init(kpw, kpb)
    src = cv2.imread("sample/output/01_2400x3200.jpg", 0)
    src = cv2.bitwise_not(src)
    src_w = np.array(src, dtype=np.float32) / 255.
    _, src_b = cv2.threshold(src_w, 0.5, 1.0, cv2.THRESH_BINARY_INV)
    _, src_f = cv2.threshold(src_w, 0.5, 1.0, cv2.THRESH_BINARY)
    _, src_w = cv2.threshold(src_w, 0.5, 1.0, cv2.THRESH_BINARY)
    th = 1.
    while 0 < th:
        th = 0.
        for i in range(8):
            src_w = cv2.filter2D(src_w, cv2.CV_32F, kpw[i])
            src_b = cv2.filter2D(src_b, cv2.CV_32F, kpb[i])
            _, src_w = cv2.threshold(src_w, 2.99, 1, cv2.THRESH_BINARY)
            _, src_b = cv2.threshold(src_b, 2.99, 1, cv2.THRESH_BINARY)
            src_w = np.array(np.logical_and(src_w, src_b), dtype=np.float32)
            th += np.sum(src_w)
            src_f = np.array(np.logical_xor(src_f, src_w), dtype=np.float32)
            src_w = src_f.copy()
            _, src_b = cv2.threshold(src_f, 0.5, 1.0, cv2.THRESH_BINARY_INV)
            cv2.imshow("process", src_w)
            cv2.waitKey(1)
    cv2.imshow("result", src_f)
    cv2.imwrite("sample/output/src_w.jpg", src_w)
    cv2.imwrite("sample/output/src_f.jpg", src_f)
