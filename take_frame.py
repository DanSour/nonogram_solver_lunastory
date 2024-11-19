import subprocess
import numpy as np
import cv2

def frame():
        
    result = subprocess.run([
        'adb', 'exec-out', 'screencap', '-p'
    ], capture_output=True, check=True)
    image_array = np.frombuffer(result.stdout, np.uint8)
    frame = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    # frame = cv2.imread(r'D:\vs_projects\nonogram_solver_lunastory\screenshots\screenshot_temp.png')
    return frame