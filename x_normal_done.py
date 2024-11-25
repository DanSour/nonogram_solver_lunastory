import time

from take_frame import frame
from detect_levels_circles import detect_circles
from detect_levels_squares import detect_squares
from detect_field import detect_puzzle
from x_big_pictures_done import tap_screen, solve_puzzle

def main(solving_type):
    try:

        puzzle = None
        circles = detect_circles(frame())  # Detect circles in the frame

        for circle in circles['circles'][::-1]:
            x = circle[0]
            y = circle[1]

            # Tap on the circle to enter the level selection
            tap_screen(x, y, delay=0.3)
            tap_screen(420, 1900, delay=1)

            for _ in range(2):
                squares = detect_squares(frame())  # Detect squares after tapping on the circle
                for square in squares['squares']:
                    x = square[0]
                    y = square[1]
                    tap_screen(x, y, delay=1)

                    puzzle = detect_puzzle(frame(), mask_type=solving_type)
                    if not solve_puzzle(puzzle['coords'], puzzle['shape']):
                        print()
                        tap_screen(90, 130, delay=0)
                        tap_screen(540, 1100, delay=1)

                    else:
                        time.sleep(0.7)
                        tap_screen(538, 1758, delay=1)
                        print('Переходим на NEXT LEVEL\n')
                
                tap_screen(660, 1900, delay=1)

            tap_screen(90, 130)

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