from ctypes import *
import math
import random
import os
import cv2
import numpy as np
import time
import detector.v4darknet


netMain = None
metaMain = None
altNames = None


def YOLO(frame_read):

    global metaMain, netMain, altNames
    configPath = "4.cfg"
    weightPath = "4.weights"
    metaPath = "coco.data"
    if not os.path.exists(configPath):
        raise ValueError("Invalid config path `" +
                         os.path.abspath(configPath)+"`")
    if not os.path.exists(weightPath):
        raise ValueError("Invalid weight path `" +
                         os.path.abspath(weightPath)+"`")
    if not os.path.exists(metaPath):
        raise ValueError("Invalid data file path `" +
                         os.path.abspath(metaPath)+"`")
    if netMain is None:
        netMain = detector.v4darknet.load_net_custom(configPath.encode(
            "ascii"), weightPath.encode("ascii"), 0, 1)  # batch size = 1
    if metaMain is None:
        metaMain = detector.v4darknet.load_meta(metaPath.encode("ascii"))
    if altNames is None:
        try:
            with open(metaPath) as metaFH:
                metaContents = metaFH.read()
                import re
                match = re.search("names *= *(.*)$", metaContents,
                                  re.IGNORECASE | re.MULTILINE)
                if match:
                    result = match.group(1)
                else:
                    result = None
                try:
                    if os.path.exists(result):
                        with open(result) as namesFH:
                            namesList = namesFH.read().strip().split("\n")
                            altNames = [x.strip() for x in namesList]
                except TypeError:
                    pass
        except Exception:
            pass

    img_h, img_w = frame_read.shape[:2]
    net_h = detector.v4darknet.network_height(netMain)
    net_w = detector.v4darknet.network_width(netMain)
    scale_h = img_h / net_h
    scale_w = img_w / net_w
    darknet_image = detector.v4darknet.make_image(net_w, net_h, 3)
    frame_rgb = cv2.cvtColor(frame_read, cv2.COLOR_BGR2RGB)
    frame_resized = cv2.resize(frame_rgb, (net_w, net_h), interpolation=cv2.INTER_LINEAR)
    detector.v4darknet.copy_image_from_bytes(darknet_image,frame_resized.tobytes())
    return detector.v4darknet.detect_image(netMain, metaMain, darknet_image, scale_h, scale_w, thresh=0.25)


if __name__ == "__main__":
    YOLO()
