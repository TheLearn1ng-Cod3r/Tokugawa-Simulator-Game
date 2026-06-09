import platform, subprocess
'''Utility functions for Japan-related operations.'''
def clear():
    # Detect the operating system
    command = "cls" if platform.system() == "Windows" else "clear"
    # Execute the command safely
    subprocess.run([command], shell=True)
