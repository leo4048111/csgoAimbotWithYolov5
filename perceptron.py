import cv2
import numpy as np
import win32api
import win32con
import win32gui
import win32ui

from options import opt

def perceptron(hwin, region=None):
    tl_x, tl_y, width, height = region
    tl_detect_x = tl_x + int((width - opt.detection_region_width) / 2)
    tl_detect_y = tl_y + int((height - opt.detection_region_height) / 2)
    hwindc = win32gui.GetWindowDC(hwin)
    srcdc = win32ui.CreateDCFromHandle(hwindc)
    memdc = srcdc.CreateCompatibleDC()
    bmp = win32ui.CreateBitmap()
    bmp.CreateCompatibleBitmap(srcdc, width, height)
    memdc.SelectObject(bmp)
    memdc.StretchBlt((0, 0), (width, height), srcdc, (tl_detect_x, tl_detect_y), (opt.detection_region_width, opt.detection_region_height), win32con.SRCCOPY)
    signedIntsArray = bmp.GetBitmapBits(True)
    img = np.fromstring(signedIntsArray, dtype='uint8')
    img.shape = (height, width, 4)

    srcdc.DeleteDC()
    memdc.DeleteDC()
    win32gui.ReleaseDC(hwin, hwindc)
    win32gui.DeleteObject(bmp.GetHandle())

    return img
