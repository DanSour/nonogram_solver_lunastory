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
    
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    field_contour = max(contours, key=cv2.contourArea)
    
    x, y, w, h = cv2.boundingRect(field_contour)

    return [[x, x+w], [y, y+h]]
