# Путь к adb
# $adbPath = ".\scrcpy-win64-v2.7\adb.exe"

# Команды tap
for ($y = 3; $y -le 22; $y++) {
    for ($x = 1; $x -le 10; $x++) {
        # & $adbPath shell input tap ($x * 100) ($y * 100)
        & adb shell input tap ($x * 100) ($y * 100)
        Start-Sleep -Milliseconds 100  # Небольшая задержка между командами, если нужно
    }
}
