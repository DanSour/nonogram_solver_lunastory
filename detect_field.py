import cv2
import numpy as np

def detect_picture(image):
    # Создаем маску для основного поля
    field_mask = cv2.inRange(image, (90, 90, 90), (255, 255, 255))
    # Ищем контуры основного поля
    contours, _ = cv2.findContours(field_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    field_contour = max(contours, key=cv2.contourArea)

    x, y, w, h = cv2.boundingRect(field_contour)

    crop = image[y:y+h, x:x+w]
    # mask = cv2.inRange(crop, (250, 250, 250), (255, 255, 255))
    mask = cv2.Canny(crop, 199, 255)
    cv2.imshow('mask', mask)
    cv2.waitKey(0)
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    # contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    square_centers = []
    for i, cnt in enumerate(contours):
        # Используем иерархию, чтобы проверить, является ли контур внешним
        if hierarchy[0][i][3] == -1:
            cnt_x, cnt_y, cnt_w, cnt_h = cv2.boundingRect(cnt)
            aspect_ratio = float(w) / h
            area = cv2.contourArea(cnt)
    
    # Ищем контуры квадратиков внутри, чтобы определить размер (15*15 или 20*20)
    # Проверяем что контур примерно квадратный (соотношение сторон близко к 1) и количество точек не больше 15
            # if 0.95 <= aspect_ratio <= 1.05 and area>3500 and len(cnt) < 15:
            #     print(area)
            #     print(len(cnt))
            #     cv2.drawContours(crop, [cnt], -1, (255, 0, 255), 3)
            #     cv2.imshow('crop', crop)
            #     cv2.waitKey(0)

            if 0.95 <= aspect_ratio <= 1.05 and area>3500 and len(cnt) < 15:
                center_x = cnt_x + cnt_w // 2
                center_y = cnt_y + cnt_h // 2
                square_centers.append([x+center_x, y+center_y])

    return {'squares':square_centers, 'coords':[[x, x+w], [y, y+h]]}


def detect_puzzle(img, mask_type='big'):

    masks = {
        'dmf': cv2.inRange(img, (70, 47, 39), (255, 255, 255)),
        'normal': cv2.inRange(img, (95, 69, 66), (255, 255, 255)),
        'big': cv2.inRange(img, (108, 93, 17), (255, 255, 255)),
    }


    contours, _ = cv2.findContours(masks[mask_type], cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    field_contour = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(field_contour)

    img = img[y:y+h, x:x+w]

    masks = {
        'dmf': cv2.inRange(img, (70, 47, 39), (255, 255, 255)),
        'normal': cv2.inRange(img, (95, 69, 66), (255, 255, 255)),
        'big': cv2.inRange(img, (108, 93, 17), (255, 255, 255)),
    }

    mask = masks[mask_type]

    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return {'coords':[[x, x+w], [y, y+h]], 'shape':int(len(contours)**0.5)}


# from take_frame import frame

# img = frame()
# picture = detect_picture(frame())

# for i in picture['squares']:
#     cv2.circle(img, i, 10, (255, 0, 255), -1)
# cv2.imshow('img', cv2.resize(img, (0, 0), fx=0.5, fy=0.5))
# cv2.waitKey(0)
