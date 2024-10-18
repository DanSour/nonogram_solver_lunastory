import subprocess

# command = "cd vs_projects/nonogram_solver_lunastory/scrcpy-win64-v2.7 ; \
command = 'adb exec-out screencap -p > \
    D:/vs_projects/nonogram_solver_lunastory/screenshots/screenshot.png '

result = subprocess.run(["pwsh", "-Command", command], check=False)
