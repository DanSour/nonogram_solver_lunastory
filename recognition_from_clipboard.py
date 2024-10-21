import pytesseract
import cv2
import win32clipboard
from PIL import ImageGrab
import numpy as np
# pip install pillow pywin32 

def get_image_from_clipboard():
    # Попытка открытия буфера обмена
    try:
        win32clipboard.OpenClipboard()
        # Проверяем, есть ли изображение в буфере обмена
        if win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_DIB):
            # Получаем изображение из буфера обмена
            image = ImageGrab.grabclipboard()
            if image is not None:
                # Преобразуем изображение Pillow в формат, пригодный для cv2
                image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
                return image
    except Exception as e:
        print(f"Ошибка при работе с буфером обмена: {e}")
    finally:
        # Закрываем буфер обмена, если он был открыт
        try:
            win32clipboard.CloseClipboard()
        except:
            pass
    return None

# Получаем изображение из буфера обмена
image = get_image_from_clipboard()
if image is not None:
    # Отображение изображения с помощью cv2
    cv2.imshow('Image from Clipboard', image)

    custom_config = '--psm 6 digits'
    result = pytesseract.image_to_string(image, config=custom_config)
    print(result)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("Буфер обмена не содержит изображение.")
