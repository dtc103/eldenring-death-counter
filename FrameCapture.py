import time
import pygetwindow as gw
from mss import mss
from multiprocessing import Event
import cv2
import numpy as np


class FrameCapture:
    def __init__(self, window_name, save_queue):
        self.width_screen_cut = 950
        self.height_screen_cut = 650

        self.queue = save_queue
        self.window_name = window_name

    def save_screenshot(self):
        active_window = gw.getActiveWindow()
        if active_window is not None and self.window_name in active_window.title.lower():
            try:
                #prepare picture for better ocr
                img = self.capture_frame()
                img = np.array(img)
                img = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
                img = cv2.convertScaleAbs(img, alpha=3.0, beta=0)

                self.queue.put(img)
            except Exception as e:
                print("Window not found")
                time.sleep(5)
                
    def capture_frame(self):
        with mss() as sct:
            #it is faster to do prechose the monitor, than getting the whole monitor and then choose the region, because it whould choose from multiple windows
            win = sct.monitors[1]
            win_dim = {"left": win["left"] + self.width_screen_cut, "top": win["top"] + self.height_screen_cut, "width": win["width"] - 2*self.width_screen_cut, "height": win["height"] - 2*self.height_screen_cut}
            sct_img = sct.grab(win_dim)
            return sct_img
        
