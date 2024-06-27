import sys
from PyQt5 import QtWidgets, QtCore, QtGui
import time
import json

class TransparentWindow(QtWidgets.QWidget):
    def __init__(self, found_event, stop_event):
        super().__init__()
        #find a way to make relative when calling script from batch file
        self.kill_counter_file = "E:/programming/EldenRingDeathCounter/deaths.json"
        self.found_event = found_event
        self.stop_event = stop_event
        self.initUI()

    def initUI(self):
        # Set the window flags to make the window frameless and always on top
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint | QtCore.Qt.Tool)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        screen_size = QtWidgets.QApplication.primaryScreen().size()

        # Label to display the number
        self.label = QtWidgets.QLabel(self)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setStyleSheet("QLabel { font-size: 40px; color: 'white' }")

        # Set geometry of the window: x, y, width, height
        self.setGeometry(int(screen_size.width() * 0.90), 0, 300, 100)

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.updateNumber)
        self.timer.start(100)  # Update the number every 1000 milliseconds (1 second)

        self.counter_text = "Deaths:"
        self.current_number = self.read_number()
        self.label.setText(str(f"{self.counter_text} {self.current_number}"))

        self.close_timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.check_stop_event)
        self.timer.start(100)

    def paintEvent(self, event):
        pass
    
    def check_stop_event(self):
        if self.stop_event.is_set():
            self.close()

    def updateNumber(self):
        if self.found_event.is_set():
            self.current_number += 1  # Increment the number
            self.label.setText(str(f"{self.counter_text} {self.current_number}"))
            self.write_number(self.current_number)
            time.sleep(4)

            self.found_event.clear()

    def read_number(self):
        with open(self.kill_counter_file) as f:
            data = json.load(f)

            num = int(data["deaths"])
            return num
        

    def write_number(self, number):
        with open(self.kill_counter_file) as f:
            data = json.load(f)

            data["deaths"] = str(number)

        with open(self.kill_counter_file, 'w') as f:
            json.dump(data, f)


    