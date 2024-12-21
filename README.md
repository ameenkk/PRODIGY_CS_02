# Image Encryption Tool

This application allows users to encrypt and decrypt images using a basic XOR operation. The app provides a simple user interface built using PyQt5. It supports various image formats such as JPG, PNG, and JPEG, and includes features like image preview, encryption, decryption, and image download.

## Features
- Upload images (JPG, PNG, JPEG).
- Encrypt images using XOR encryption.
- Decrypt images back using the same key.
- Image preview before and after encryption or decryption.
- Save the processed image to your local disk.

## Requirements
- Python 3.x
- PyQt5
- OpenCV
- NumPy
- Pillow

## Installation
1. Clone or download the repository.
2. Install the required dependencies using pip:
    ```bash
    pip install PyQt5 opencv-python numpy pillow
    ```

## Usage
1. Run the application:
    ```bash
    python pixel.py
    ```
2. Upload an image by clicking the "Upload Image" button.
3. Enter an encryption key (alphanumeric).
4. Click "Encrypt Image" to encrypt the image.
5. Click "Decrypt Image" to decrypt the image using the same key.
6. Download the processed image by clicking the "Download Image" button.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
