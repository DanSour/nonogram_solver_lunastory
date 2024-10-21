import subprocess

path_to_save = 'D:/vs_projects/nonogram_solver_lunastory/screenshots/screenshot.png '

# def screenshot(path_to_save):
# command = "cd vs_projects/nonogram_solver_lunastory/scrcpy-win64-v2.7 ; \
command = 'adb exec-out screencap -p > '+path_to_save

# result = subprocess.run(["pwsh", "-Command", command], check=False)
subprocess.run(["pwsh", "-Command", command], check=False)


def screenshot(path_to_save):
    
    command = 'adb exec-out screencap -p > '+path_to_save
    subprocess.run(["pwsh", "-Command", command], check=False)

    return 
