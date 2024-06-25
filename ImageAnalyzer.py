import easyocr

class ImageAnalyzer:
    def __init__(self, check_text, language="en"):
        self.check_text = check_text
        self.reader = easyocr.Reader([language], gpu=True)

    def check_image_for_text(self, image, text):
        results = self.reader.readtext(image)

        for _, img_text, prob in results:
            if img_text in text and prob > 0.7:
                return True
        return False
    
    