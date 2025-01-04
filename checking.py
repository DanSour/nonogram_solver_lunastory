import cv2 
import time
import subprocess
import pytesseract
from take_frame import frame


def check_complete(image):

    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY_INV)[1]

    result = pytesseract.image_to_string(image)

    return 'COMPLETE' in result


def try_solve_with_hints(height, width):
    # Используем подсказки
    for _ in range(5):
        subprocess.run(["pwsh", "-Command", f'adb shell input tap {0.95 * width} {0.65 * height}'], check=False)

    time.sleep(1)
    return check_complete(frame())


def check_is_enter(image, custom_config=r'--oem 3 --psm 6'):

    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY_INV)[1]

    cropped = image[690:780, 360:720]

    result = pytesseract.image_to_string(cropped, config=custom_config)

    return 'BIG' not in result
