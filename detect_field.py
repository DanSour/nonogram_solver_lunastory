import cv2

def detect_field_coords(image):
    # Конвертируем BGR в RGB
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Создаем маску для основного поля
    # For LunaStory
    # mask = cv2.inRange(rgb, (105, 145, 160), (170, 205, 205))
    # For DeerMyFriend
    # mask = cv2.inRange(rgb, (55, 66, 85), (255, 255, 255))
    
    mask = cv2.inRange(rgb, (90, 90, 90), (255, 255, 255))
    
    # rgb = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # mask = cv2.threshold(rgb, 114, 255, cv2.THRESH_BINARY)[1] # ориг

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    field_contour = max(contours, key=cv2.contourArea)
    
    x, y, w, h = cv2.boundingRect(field_contour)

    return [[x, x+w], [y, y+h]]

# def draw_field_contours(image, coords):
#     x1, y1, x2, y2 = coords[0][0], coords[1][0], coords[0][1], coords[1][1]
#     cv2.rectangle(image, (x1, y1), (x2, y2), (255, 00, 255), 2)
#     cv2.imshow('image', cv2.resize(image, (0, 0), fx=0.5, fy=0.5))
#     cv2.waitKey(0)
#     return image
