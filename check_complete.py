import cv2 
import pytesseract



def competition(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    cropped = image[690:780, 360:720]

    # custom_config = '--psm 6 digits'
    result = pytesseract.image_to_string(cropped) 
                                        #  config=custom_config)
    return result == 'COMPLETE\n' 

    # cv2.imshow('cropped', cropped)
    # cv2.waitKey(0)



# image_path = f"D:/vs_projects/nonogram_solver_lunastory/screenshots/screenshot.png"
    
# image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
# image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

# cropped = image[690:780, 360:720]

# # custom_config = '--psm 6 digits'
# result = pytesseract.image_to_string(cropped) 
#                                     #  config=custom_config)
# print(result == 'COMPLETE\n')

# cv2.imshow('cropped', cropped)
# cv2.waitKey(0)