import cv2
import pytesseract

def is_enter(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    # image = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY_INV)[1]

    image = image[690:760, 470:600]

    custom_config = r'--oem 3 --psm 6'
    result = pytesseract.image_to_string(image, config=custom_config)
    # print(result)
    return result != 'BIG\n'

    # cv2.imshow('image', image)
    # cv2.waitKey(0)

# path = 'D:/vs_projects/nonogram_solver_lunastory/screenshots/screenshot.png'
# print(is_enter(path))