import subprocess

# Пример команды для выполнения в pwsh через Python

taps = ''
for y in range(3, 23):
    for x in range(1, 11):
        # Записать все в одну строку и выполнить одну большую команду разом
        taps += f"adb shell input tap {x}00 {y}00 ; "
    
subprocess.run(["pwsh", "-Command", taps[:-2]], check=False)