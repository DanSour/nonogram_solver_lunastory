import time

from take_frame import frame
from detect_levels_circles import detect_circles
from detect_levels_squares import detect_squares
from detect_field import detect_puzzle
from x_big_pictures_done import tap_screen, solve_puzzle

def main(solving_type):
    height, width = frame().shape[:2]
    try:

        puzzle = None
        circles = detect_circles(frame())  # Detect circles in the frame

        for circle in circles['circles']:
            x = circle[0]
            y = circle[1]

            # Tap on the circle to enter the level selection
            tap_screen(x, y, delay=0.2)
            tap_screen(int(0.38525*width), int(0.79277*height), delay=0.3)

            for _ in range(2):
                squares = detect_squares(frame())  # Detect squares after tapping on the circle
                for square in squares['squares']:
                    x = square[0]
                    y = square[1]
                    tap_screen(x, y, delay=1)

                    try:
                        puzzle = detect_puzzle(frame(), mask_type=solving_type)
                    except Exception as e:
                        print(f"Произошла ошибка в файле detect_puzzle: {e}")
                        tap_screen(int(0.08333*width), int(0.05417*height), delay=0.01)
                        tap_screen(int(0.5*width), int(0.45833*height), delay=1)
                        continue

                    if not solve_puzzle(puzzle['coords'], puzzle['shape'], height, width):
                        print()
                        tap_screen(int(0.08333*width), int(0.05417*height), delay=0)
                        tap_screen(int(0.5*width), int(0.45833*height), delay=1)

                    else:
                        time.sleep(0.7)
                        tap_screen(int(0.49815*width), int(0.73250*height), delay=1)
                        print('Переходим на NEXT LEVEL\n')
                
                tap_screen(int(0.61111*width), int(0.79167*height), delay=1)

            tap_screen(int(0.08333*width), int(0.05417*height))

    except Exception as e:
        print(f"Произошла ошибка в файле normal_done: {e}")

if __name__ == '__main__':

    start_time = time.time()
    solving_type = 'normal'
    main(solving_type)
    end_time = time.time()

    elapsed_time = end_time - start_time
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)

    print(f"{minutes} минут {seconds} секунд")