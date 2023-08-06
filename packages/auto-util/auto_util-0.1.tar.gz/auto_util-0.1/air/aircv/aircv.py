#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import cv2
import numpy as np
from .error import FileNotExistError
from six import PY2, PY3


def imread(filename, flatten=False):
    """根据图片路径，将图片读取为cv2的图片处理格式."""
    if not os.path.isfile(filename):
        raise FileNotExistError("File not exist: %s" % filename)

    # choose image readin mode: cv2.IMREAD_UNCHANGED=-1, cv2.IMREAD_GRAYSCALE=0, cv2.IMREAD_COLOR=1,
    readin_mode = cv2.IMREAD_GRAYSCALE if flatten else cv2.IMREAD_COLOR

    if PY3:
        img = cv2.imdecode(np.fromfile(filename, dtype=np.uint8), readin_mode)
    else:
        filename = filename.encode(sys.getfilesystemencoding())
        img = cv2.imread(filename, readin_mode)

    return img

