import easyocr
from multiprocessing import Process
import numpy as np
import cv2

class ImageAnalyzerProcess:
    def __init__(self, img_queue_read, img_queue_write, check_text, process_ready, found_event, stop_event, language="en"):
        self.check_text = check_text
        
        
        self.queue_read = img_queue_read
        self.queue_write = img_queue_write
        self.check_text = check_text

        self.process_ready = process_ready
        self.found_event = found_event
        self.stop_event = stop_event

        self.analyzer_process = Process(target=self.analyzer_task, args=(self.check_text, self.queue_read, self.queue_write, self.process_ready, self.found_event, self.stop_event))
        self.analyzer_process.daemon = True
        self.analyzer_process.start()

    def check_image_for_text(self, reader, image, text):
        results = reader.readtext(image)

        for _, img_text, prob in results:
            if img_text in text and prob > 0.7:
                return True

        return False
    
    def analyzer_task(self, check_text, read_queue, write_queue, process_ready, found_event, stop_event):
        reader = easyocr.Reader(["en"], gpu=True)

        with process_ready.get_lock():
            process_ready.value = True
        
        while not stop_event.is_set():
            if not read_queue.empty():
                img = read_queue.get()
                if self.check_image_for_text(reader, img, check_text):
                    write_queue.put(img)

                    found_event.set()