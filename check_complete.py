import cv2 
import pytesseract


def competition(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    image = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY_INV)[1]

    cropped = image[690:780, 360:720]
    result = pytesseract.image_to_string(cropped) 
    
    return result[:-1] == 'COMPLETE'
