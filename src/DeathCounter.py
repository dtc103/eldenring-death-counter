from FrameCapturer import FrameCapturer
from ImageAnalyzer import ImageAnalyzer
from multiprocessing import Queue, Process, Value, Event, Manager
import time
import psutil
import pygetwindow as gw

class DeathCounter:
    def __init__(self, process_name, window_name, monitor_idx, fps=5):
        self.check_text = "YOU DIED"
        self.process_name = process_name
        self.window_name = window_name
        self.fps = fps
        self.monitor_idx = monitor_idx

        self.capture_queue = Queue()
        # event set when ocr found the death screen
        self.found_event = Event()
        # event set when game crashes or game stopped
        self.stop_event = Event()

        self.analyzer_ready1 = Value('b', False)
        self.analyzer_ready2 = Value('b', False)
        self.observer_ready = Value('b', False)

        self.analyzer_process1 = Process(target=DeathCounter.analyzer_task, args=(self.check_text, self.capture_queue, self.analyzer_ready1, self.found_event, self.stop_event))
        #self.analyzer_process2 = Process(target=DeathCounter.analyzer_task, args=(self.check_text, self.capture_queue, self.analyzer_ready2, self.found_event, self.stop_event))
        self.observer_process = Process(target=DeathCounter.observer_task, args=("eldenring.exe", "elden ring", self.monitor_idx, self.fps, self.capture_queue, self.stop_event))
        
    def start(self):
        self.analyzer_process1.start()
        #self.analyzer_process2.start()
        print("Started process")
        self.wait_until_variable(self.analyzer_ready1, True, 30)
        #self.wait_until_variable(self.analyzer_ready2, True, 30)
        self.observer_process.start()
    
    def stop(self):
        self.stop_event.set()

    def wait_until_variable(self, variable, desired_state, timeout):
        #wait until analyzer process is launched
        start = time.time()
        while True:
            if variable.value == desired_state:
                break
            time.sleep(1)
            if time.time() - start > timeout:
                raise TimeoutError("Process creation timed out")

    @staticmethod
    def is_application_running(process_name):
        for process in psutil.process_iter(['name']):
            if process_name.lower() in process.info['name'].lower():
                return True
        return False


    @staticmethod
    def observer_task(process_name, window_name, monitor_idx, fps, capture_queue, stop_event):
        while not DeathCounter.is_application_running(process_name):
            time.sleep(5)
        
        fc = FrameCapturer(monitor_idx)

        while DeathCounter.is_application_running(process_name) and not stop_event.is_set():
            active_window = gw.getActiveWindow()
            if active_window is not None and window_name in active_window.title.lower():
                capture_queue.put(fc.save_screenshot())
            time.sleep(1 / fps)

        #if application crashes or stops, also stop the programm
        stop_event.set()

    @staticmethod
    def analyzer_task(check_text, image_queue, process_ready, found_event, stop_event):
        ia = ImageAnalyzer(check_text=check_text)

        # process is ready
        process_ready.value = True
        
        while not stop_event.is_set():
            if not image_queue.empty():
                img = image_queue.get()
                if ia.check_image_for_text(img, check_text):
                    found_event.set()
