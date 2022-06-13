from time import sleep

import cv2
import win32api
import win32gui
import win32con
import threading

from perceptron import perceptron
from detection import detection
from controller import aimAt
from gui import gui_main

window_name = 'csgo-detect'

def main():
    hwin = None
    while not hwin:
        hwin = win32gui.FindWindow(None, 'Counter-Strike: Global Offensive - Direct3D 9')
        print("Waiting for csgo...")
        sleep(1)
    print("Aimbot is running...")
    windowRect = win32gui.GetWindowRect(hwin)
    caption_height = win32api.GetSystemMetrics(win32con.SM_CYCAPTION)
    screen_X1 = win32api.GetSystemMetrics(win32con.SM_CXFULLSCREEN)
    screen_X2 = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
    screen_Y1 = win32api.GetSystemMetrics(win32con.SM_CYFULLSCREEN)
    screen_Y2 = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)


    # tl_x and tl_y is the top_left coord for window client space
    tl_x, tl_y, br_x, br_y = windowRect
    tl_y = tl_y
    window_width = screen_width = br_x - tl_x
    window_height = screen_height = br_y - tl_y
    thread = threading.Thread(target=gui_main, args=())
    thread.start()
    # main loop
    while True:
        img0 = perceptron(hwin, region=(tl_x, tl_y, screen_width, screen_height))  # Get 1 frame image with preceptron
        img0 = cv2.resize(img0, (window_width, window_height))
        img = cv2.cvtColor(img0, cv2.COLOR_BGRA2RGB)
        result = detection(img)  # format: [label, x_center, y_center, width, height], get detection result
        if len(result):
            aimAt(result, window_width, window_height)
            for i, det in enumerate(result):
                tag, x_center, y_center, width, height = det
                tag = int(tag)
                x_center, width = screen_width * float(x_center), screen_width * float(width)  # unnormalize
                y_center, height = screen_height * float(y_center), screen_height * float(height)
                box_tl = (int(x_center - width / 2.), int(y_center - height / 2.))
                box_br = (int(x_center + width / 2.), int(y_center + height / 2.))
                label_names = ['CT', 'CT_HEAD', 'T', 'T_HEAD']
                if tag == 0 or tag == 2:
                    color = (0, 255, 255)
                else:
                    color = (0, 0, 255)
                cv2.rectangle(img0, box_tl, box_br, color=color, thickness=3)
                cv2.putText(img=img0, text=label_names[tag], org=(box_tl[0], box_tl[1] - 5),
                            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                            fontScale=1,
                            color=color, thickness=3, lineType=cv2.LINE_AA)

        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)  # 打开新窗口
        cv2.resizeWindow(window_name, window_width // 2, window_height // 2)
        cv2.imshow(window_name, img0)

        hwnd = win32gui.FindWindow(None, window_name)
        win32gui.SetWindowPos(hwnd,
                              win32con.HWND_TOPMOST,
                              0, 0, 0, 0,
                              win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break


if __name__ == "__main__":
    main()
