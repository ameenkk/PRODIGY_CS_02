import sys
import os
import random
import string
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QFileDialog, QComboBox, QProgressBar, QHBoxLayout
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
from PIL import Image

# Utility Functions
def generate_key(length=10):
    """Generates a random alphanumeric key."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def save_image(img, path):
    """Saves the image to a given path."""
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)  # Convert back to BGR for saving
    cv2.imwrite(path, img)


def xor_encrypt(image_path, key):
    """Encrypts the image using XOR operation and the provided key."""
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert to RGB format

    key_int = sum(ord(char) for char in key)  # Convert key to a numerical value
    encrypted_img = np.copy(img)

    # XOR operation on each pixel
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            for c in range(3):  # RGB channels
                encrypted_img[i, j, c] ^= key_int % 256

    return encrypted_img


# PyQt5 Application Class
class ImageEncryptionApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Image Encryption Tool")
        self.setGeometry(100, 100, 700, 600)
        self.image_path = None
        self.processed_image = None
        self.processed_image_path = None
        self.mode = "Light"

        # Layout and widgets initialization
        self.init_ui()

    def init_ui(self):
        """Sets up the user interface components."""
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)

        # File picker button with icon
        self.file_picker_button = QPushButton()
        self.file_picker_button.setIcon(QIcon("upload_icon.png"))  # Set an icon (you need to provide an upload_icon.png)
        self.file_picker_button.setText("Upload Image")
        self.file_picker_button.setStyleSheet(self.get_button_style())
        self.file_picker_button.clicked.connect(self.upload_image)

        # Image preview
        self.image_label = QLabel("No image selected.")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("border: 1px solid #cccccc; border-radius: 8px; padding: 10px; margin-top: 20px;")

        # Key input field
        self.key_input = QLineEdit()
        self.key_input.setPlaceholderText("Enter Encryption Key")
        self.key_input.setStyleSheet(self.get_input_style())

        # Encryption method dropdown
        self.method_selector = QComboBox()
        self.method_selector.addItems(['XOR'])
        self.method_selector.setStyleSheet(self.get_input_style())

        # Encrypt and Decrypt buttons with hover effect
        self.encrypt_button = QPushButton("Encrypt Image")
        self.encrypt_button.setStyleSheet(self.get_button_style())
        self.encrypt_button.clicked.connect(self.encrypt_image)

        self.decrypt_button = QPushButton("Decrypt Image")
        self.decrypt_button.setStyleSheet(self.get_button_style())
        self.decrypt_button.clicked.connect(self.decrypt_image)

        # Download button
        self.download_button = QPushButton("Download Image")
        self.download_button.setStyleSheet(self.get_button_style())
        self.download_button.setEnabled(False)  # Disabled until image is processed
        self.download_button.clicked.connect(self.download_image)

        # Progress Bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)
        self.progress_bar.setStyleSheet("QProgressBar { border-radius: 8px; background: #f2f2f2; }")

        # Result label
        self.result_label = QLabel("")
        self.result_label.setAlignment(Qt.AlignCenter)

        # Dark/Light mode toggle button
        self.toggle_mode_button = QPushButton(f"Switch to Dark Mode")
        self.toggle_mode_button.setStyleSheet(self.get_button_style())
        self.toggle_mode_button.clicked.connect(self.toggle_mode)

        # Add widgets to layout
        self.layout.addWidget(self.file_picker_button)
        self.layout.addWidget(self.image_label)
        self.layout.addWidget(self.key_input)
        self.layout.addWidget(self.method_selector)
        self.layout.addWidget(self.encrypt_button)
        self.layout.addWidget(self.decrypt_button)
        self.layout.addWidget(self.download_button)
        self.layout.addWidget(self.progress_bar)
        self.layout.addWidget(self.toggle_mode_button)
        self.layout.addWidget(self.result_label)

        self.setLayout(self.layout)

    def get_button_style(self):
        """Returns a consistent modern button style."""
        return """
        QPushButton {
            background-color: #4CAF50;
            color: white;
            border-radius: 10px;
            padding: 12px 24px;
            font-size: 16px;
            font-weight: bold;
            margin: 10px;
        }
        QPushButton:hover {
            background-color: #45a049;
        }
        QPushButton:disabled {
            background-color: #d3d3d3;
            color: #9e9e9e;
        }
        """

    def get_input_style(self):
        """Returns a consistent modern input field style."""
        return """
        QLineEdit, QComboBox {
            background-color: #f9f9f9;
            border-radius: 8px;
            padding: 10px;
            font-size: 16px;
            margin-top: 10px;
            border: 1px solid #cccccc;
        }
        """

    def upload_image(self):
        """Handles image file upload."""
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        file_dialog.setNameFilter("Images (*.jpg *.jpeg *.png)")
        if file_dialog.exec_():
            file_paths = file_dialog.selectedFiles()
            if file_paths:
                self.image_path = file_paths[0]
                self.image_label.setText(f"Selected file: {os.path.basename(self.image_path)}")
                self.display_image(self.image_path)

    def encrypt_image(self):
        """Handles the image encryption process."""
        if not self.image_path:
            self.result_label.setText("Please upload an image first.")
            return

        key = self.key_input.text()
        if not key:
            self.result_label.setText("Please enter an encryption key.")
            return

        self.progress_bar.setVisible(True)

        self.processed_image = None
        self.processed_image_path = "processed_image.png"

        # XOR encryption
        self.processed_image = xor_encrypt(self.image_path, key)

        save_image(self.processed_image, self.processed_image_path)
        self.result_label.setText(f"Image encrypted successfully using XOR!")
        self.download_button.setEnabled(True)

    def decrypt_image(self):
        """Handles the image decryption process."""
        if not self.image_path:
            self.result_label.setText("Please upload an image first.")
            return

        key = self.key_input.text()
        if not key:
            self.result_label.setText("Please enter an encryption key.")
            return

        self.processed_image = xor_encrypt(self.image_path, key)  # XOR decryption is the same as encryption
        self.processed_image_path = "decrypted_image.png"
        save_image(self.processed_image, self.processed_image_path)
        self.result_label.setText(f"Image decrypted successfully using XOR!")
        self.download_button.setEnabled(True)

    def download_image(self):
        """Handles downloading the processed image."""
        if not self.processed_image_path:
            self.result_label.setText("No image to download.")
            return

        save_path, _ = QFileDialog.getSaveFileName(self, "Save Image", self.processed_image_path, "Images (*.png *.jpg *.jpeg)")
        if save_path:
            save_image(self.processed_image, save_path)
            self.result_label.setText(f"Image saved as {os.path.basename(save_path)}")
            self.download_button.setEnabled(False)

    def display_image(self, image_path):
        """Displays the image in the UI."""
        pixmap = QPixmap(image_path)
        pixmap = pixmap.scaled(300, 300, Qt.KeepAspectRatio)
        self.image_label.setPixmap(pixmap)
        self.image_label.setAlignment(Qt.AlignCenter)

    def toggle_mode(self):
        """Toggles between light and dark modes."""
        if self.mode == "Light":
            self.setStyleSheet("background-color: #2E2E2E; color: white;")
            self.toggle_mode_button.setText("Switch to Light Mode")
            self.mode = "Dark"
        else:
            self.setStyleSheet("background-color: white; color: black;")
            self.toggle_mode_button.setText("Switch to Dark Mode")
            self.mode = "Light"


# Main Program Execution
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageEncryptionApp()
    window.show()
    sys.exit(app.exec_())
