import cv2 
import pytesseract


def competition(image):
    # image = cv2.imread(image, cv2.IMREAD_GRAYSCALE)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY_INV)[1]


    result = pytesseract.image_to_string(image)

    return 'COMPLETE' in result