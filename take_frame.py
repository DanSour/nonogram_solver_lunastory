import subprocess
import numpy as np
import cv2

def frame():
    try:
        result = subprocess.run([
            'adb', 'exec-out', 'screencap', '-p'
        ], capture_output=True, check=True)
        image_array = np.frombuffer(result.stdout, np.uint8)
        frame = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        return frame
    
    except Exception as e:
        print(f"Произошла ошибка: {e}")