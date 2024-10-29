import cv2
import pytesseract

def is_enter(image, custom_config=r'--oem 3 --psm 6'):

    # image = image[690:760, 470:600]

    # # custom_config = r'--oem 3 --psm 6'
    # result = pytesseract.image_to_string(image, config=custom_config)
    
    # return result != 'BIG\n'
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY_INV)[1]

    cropped = image[690:780, 360:720]

    result = pytesseract.image_to_string(cropped, config=custom_config)

    return 'BIG' not in result

