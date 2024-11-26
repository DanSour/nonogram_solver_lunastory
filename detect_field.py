import cv2
import numpy as np

def detect_picture(image):
    try:
        # Создаем маску для основного поля
        field_mask = cv2.inRange(image, (90, 90, 90), (255, 255, 255))
        # Ищем контуры основного поля
        contours, _ = cv2.findContours(field_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        field_contour = max(contours, key=cv2.contourArea)

        x, y, w, h = cv2.boundingRect(field_contour)

        crop = image[y:y+h, x:x+w]
        mask = cv2.inRange(crop, (70, 70, 70), (255, 255, 255))
        # mask = cv2.inRange(crop, (89, 56, 48), (96, 63, 68))
        mask = cv2.bitwise_not(mask)
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
        square_centers = []
        for i, cnt in enumerate(contours):
            # Используем иерархию, чтобы проверить, является ли контур внешним
            if hierarchy[0][i][3] == -1:
                cnt_x, cnt_y, cnt_w, cnt_h = cv2.boundingRect(cnt)
                aspect_ratio = float(w) / h
                area = cv2.contourArea(cnt)
        
        # Ищем контуры квадратиков внутри, чтобы определить размер (15*15 или 20*20)
        # Проверяем что контур примерно квадратный (соотношение сторон близко к 1) и количество точек не больше 15
                if 0.95 <= aspect_ratio <= 1.05 and area>3500 and len(cnt) < 15:
                    center_x = cnt_x + cnt_w // 2
                    center_y = cnt_y + cnt_h // 2
                    square_centers.append([x+center_x, y+center_y])
        return {'squares':square_centers, 'coords':[[x, x+w], [y, y+h]]}
    
    except Exception as e:
        print(f"Error in detect_picture: {e}")
        return {'squares':square_centers, 'coords':[[x, x+w], [y, y+h]]}

def detect_puzzle(img, mask_type='big'):
    try:

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

        contours, _ = cv2.findContours(mask, cv2.RETR_LIST , cv2.CHAIN_APPROX_SIMPLE)

    except Exception as e:
        print(f"Error in detect_puzzle: {e}")
        return {'coords':[[x, x+w], [y, y+h]], 'shape':int(len(contours)**0.5)}
    
    return {'coords':[[x, x+w], [y, y+h]], 'shape':int(len(contours)**0.5)}
