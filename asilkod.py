import tkinter as tk
from PIL import Image, ImageTk, ImageGrab
import pytesseract
import cv2
import numpy as np
import pyautogui
import keyboard
# Set the path to the Tesseract OCR executable (replace with your path)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

class MouseClickApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Ekran Görüntüsü ve Fare Tıklamaları")
        self.master.geometry("{0}x{1}".format(self.master.winfo_screenwidth(), self.master.winfo_screenheight()))

        self.start_point = None
        self.end_point = None

        self.screenshot_image = ImageGrab.grab()
        self.screenshot_image = ImageTk.PhotoImage(self.screenshot_image)

        self.canvas = tk.Canvas(self.master, bg="white", highlightthickness=0)
        self.canvas.create_image(0, 0, image=self.screenshot_image, anchor="nw")
        self.canvas.pack(fill="both", expand=True)

        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

    def on_click(self, event):
        self.start_point = (event.x, event.y)

    def on_drag(self, event):
        if self.start_point:
            x, y = event.x, event.y
            self.canvas.delete("rectangle")
            self.canvas.create_rectangle(self.start_point[0], self.start_point[1], x, y, outline="blue", tags="rectangle")

    def on_release(self, event):
        if self.start_point:
            self.end_point = (event.x, event.y)
            x1, y1 = self.start_point
            x2, y2 = self.end_point

            # Kare içindeki ekran görüntüsü alınacak bölgeyi hesaplayın
            min_x, max_x = min(x1, x2), max(x1, x2)
            min_y, max_y = min(y1, y2), max(y1, y2)

            # Kareyi 30 piksel aşağıya kaydırın
            min_y += 39
            max_y += 37
            min_x += 12
            max_x += 8
            screen_width = self.master.winfo_screenwidth()
            screen_height = self.master.winfo_screenheight()

            # Bölgeleri ekran sınırlarına uygun şekilde düzenle
            min_x = max(min_x, 0)
            min_y = max(min_y, 0)
            max_x = min(max_x, screen_width)
            max_y = min(max_y, screen_height)

            region = (min_x, min_y, max_x, max_y)
            img = ImageGrab.grab(bbox=region)

            # Extract text from the captured image using Tesseract OCR
            extracted_text = self.extract_text_from_image(img)
            print("Extracted Text:")
            print(extracted_text)

    def extract_text_from_image(self, img):
        # Convert the PIL image to a NumPy array for use with OpenCV
        img_np = np.array(img)

        # Convert the color channels from RGB to BGR (OpenCV uses BGR format)
        img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

        # Convert the image to grayscale
        gray_img = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

        # Perform image preprocessing (optional)
        # You can experiment with different preprocessing techniques
        # before feeding the image to Tesseract for better results.

        # Use pytesseract to extract text from the preprocessed image
        extracted_text = pytesseract.image_to_string(gray_img, lang="tur")

        return extracted_text

if __name__ == "__main__":
    root = tk.Tk()
    app = MouseClickApp(root)
    root.mainloop()
