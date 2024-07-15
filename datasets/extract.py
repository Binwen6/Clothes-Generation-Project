import sys
import os
import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt

class ImageAnnotator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Annotator")
        self.setGeometry(100, 100, 1600, 1200)  # Enlarged window size

        self.image_label = QLabel(self)
        self.image_label.setGeometry(10, 10, 1580, 1160)  # Enlarged label size to match window

        self.current_image_path = ""
        self.current_image = None
        self.drawing = False
        self.ix, self.iy = -1, -1
        self.rect = None
        self.scale_factor = 1.0  # To adjust coordinates for saving

        self.image_index = 569
        self.pair_index = 723

        self.load_next_image()

    def load_next_image(self):
        image_path = f"./necklaces/model/necklace_model{self.image_index}.jpg"
        if os.path.exists(image_path):
            self.current_image_path = image_path
            self.current_image = cv2.imread(image_path)
            self.display_image()
            self.image_index += 1
        else:
            print("No more images to annotate.")
            self.close()

    def display_image(self):
        height, width, channel = self.current_image.shape
        self.scale_factor = min((self.image_label.width() - 20) / width, (self.image_label.height() - 20) / height)
        scaled_width = int(width * self.scale_factor)
        scaled_height = int(height * self.scale_factor)

        scaled_image = cv2.resize(self.current_image, (scaled_width, scaled_height))
        bytes_per_line = 3 * scaled_width
        q_image = QImage(scaled_image.data, scaled_width, scaled_height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
        pixmap = QPixmap.fromImage(q_image)
        self.image_label.setPixmap(pixmap)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.ix, self.iy = event.x() - self.image_label.x(), event.y() - self.image_label.y()

    def mouseMoveEvent(self, event):
        if self.drawing:
            x, y = event.x() - self.image_label.x(), event.y() - self.image_label.y()
            img_copy = cv2.resize(self.current_image, (int(self.current_image.shape[1] * self.scale_factor), int(self.current_image.shape[0] * self.scale_factor)))
            cv2.rectangle(img_copy, (self.ix, self.iy), (x, y), (0, 255, 0), 2)
            self.display_image_with_rect(img_copy)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = False
            x, y = event.x() - self.image_label.x(), event.y() - self.image_label.y()
            self.rect = (min(self.ix, x), min(self.iy, y), abs(x - self.ix), abs(y - self.iy))
            self.save_annotation()
            self.load_next_image()

    def display_image_with_rect(self, img):
        height, width, channel = img.shape
        bytes_per_line = 3 * width
        q_image = QImage(img.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
        pixmap = QPixmap.fromImage(q_image)
        self.image_label.setPixmap(pixmap)

    def save_annotation(self):
        if self.rect:
            pair_folder = f"./necklace_pairs/pair_{self.pair_index}"
            os.makedirs(pair_folder, exist_ok=True)

            # Adjust rectangle for original size
            rect_scaled = (int(self.rect[0] / self.scale_factor), int(self.rect[1] / self.scale_factor),
                           int(self.rect[2] / self.scale_factor), int(self.rect[3] / self.scale_factor))

            # Save original image
            cv2.imwrite(os.path.join(pair_folder, "model.jpg"), self.current_image)

            # Save cropped image
            cropped_image = self.current_image[rect_scaled[1]:rect_scaled[1] + rect_scaled[3], rect_scaled[0]:rect_scaled[0] + rect_scaled[2]]
            cv2.imwrite(os.path.join(pair_folder, "jewellery.jpg"), cropped_image)

            self.pair_index += 1
            self.rect = None

if __name__ == "__main__":
    app = QApplication(sys.argv)
    annotator = ImageAnnotator()
    annotator.show()
    sys.exit(app.exec_())
