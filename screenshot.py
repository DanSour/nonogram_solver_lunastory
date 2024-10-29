import subprocess

def screenshot(path_to_save):
    
    command = 'adb exec-out screencap -p > '+path_to_save
    subprocess.run(["pwsh", "-Command", command], check=False)

    return 

# screenshot(r'D:\vs_projects\nonogram_solver_lunastory\screenshots\screenshot_temp.png')