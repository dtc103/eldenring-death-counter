from FrameCapture import FrameCapture
from ImageAnalyzer import ImageAnalyzerProcess
#import queue
import multiprocessing
from multiprocessing import Queue, Process, Value, Event, Manager
import threading
import time
import cv2
import numpy as np
import psutil

class DeathCounter:
    def __init__(self, process_name, window_name, fps=5):
        self.check_text = "YOU DIED"

        self.capture_queue = Queue()
        self.result_queue = Queue()
        self.process_ready = Value('b', False)

        self.stop_event = Event()
        self.found_event = Event()

        self.process_name = process_name
        self.window_name = window_name
        self.fps = fps

        self.analyzer_process = ImageAnalyzerProcess(self.capture_queue, self.result_queue, self.check_text, self.process_ready, self.found_event, self.stop_event)


        self.observer_thread = threading.Thread(target=self.observer_task, args=("eldenring.exe", "elden ring", self.capture_queue, self.found_event, self.stop_event))
        self.observer_thread.daemon = True

        #wait until analyzer process is launched
        start = time.time()
        while True:
            with self.process_ready.get_lock():
                if self.process_ready.value:
                    break
            time.sleep(2)
            if time.time() - start > 60:
                raise TimeoutError("Process creation timed out")
            
        self.observer_thread.start()

    def is_application_running(self, process_name):
        for process in psutil.process_iter(['name']):
            if process_name.lower() in process.info['name'].lower():
                return True
        return False
    

    def observer_task(self, process_name, window_name, capture_queue, pause_event, stop_event):
        while not self.is_application_running(process_name):
            time.sleep(10)
        print("process is running")
        fc = FrameCapture(window_name, capture_queue)

        while self.is_application_running(process_name) and not stop_event.is_set():
            fc.save_screenshot()
            time.sleep(1 / self.fps)

        stop_event.set()

    def stop(self):
        self.stop_event.set()
