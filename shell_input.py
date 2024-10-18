import subprocess

# Пример команды для выполнения в pwsh через Python

# Запуск команды
# command = "cd vs_projects/nonogram_solver_lunastory/scrcpy-win64-v2.7 ; "

taps = ''
for y in range(3, 23):
    for x in range(1, 11):
        # Вызывать по одной команде
        # result = subprocess.run(["pwsh", "-Command", command], capture_output=True, text=True)
        # Вызывать по одной команде
        # result = subprocess.run(["pwsh", "-Command", command+f"{x}00 {y}00"])
        # Записать все в одну строку и выполнить одну большую команду разом
        # taps += f"./adb shell input tap {x}00 {y}00 ; "
        
        taps += f"adb shell input tap {x}00 {y}00 ; "
    
# line = command+taps
subprocess.run(["pwsh", "-Command", taps[:-2]], check=False)

# result = subprocess.run(["pwsh", "-Command", command], capture_output=True, text=True)