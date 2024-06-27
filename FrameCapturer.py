from mss import mss
import cv2
import numpy as np


class FrameCapturer:
    def __init__(self, monitor_idx):
        self.monitor_idx = monitor_idx

    def save_screenshot(self):
        #prepare picture for better ocr
        img = self.capture_frame()
        img = np.array(img)
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
        img = cv2.convertScaleAbs(img, alpha=3.0, beta=0)

        return img
                
    def capture_frame(self):
        with mss() as sct:
            #it is faster to do prechose the monitor, than getting the whole monitor and then choose the region, because it whould choose from multiple windows
            win = sct.monitors[self.monitor_idx]
            win_dim = self._select_area(win)
            sct_img = sct.grab(win_dim)
            return sct_img
        
    def _select_area(self, win):
        width_min, width_max = 0.35, 0.65
        height_min, height_max = 0.45, 0.55

        win_dim = {"left": int(width_min * win["width"]), "top": int(height_min * win["height"]), "width": int(width_max * win["width"] - width_min * win["width"]), "height": int(height_max * win["height"] - height_min * win["height"])}

        return win_dim