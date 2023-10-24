import subprocess
import platform
import os
from pathlib import Path

script_directory = Path(os.path.abspath(__file__)).parent.parent

if platform.system() != 'Windows':
    activate_script = Path(script_directory, 'venv', 'bin')
    run_command = f'cd {script_directory};cd {activate_script};{activate_script};cd {script_directory};python bot.py'
else:
    activate_script = Path(script_directory, 'venv', 'Scripts')
    run_command = f'cd {script_directory} && cd {activate_script} && activate && cd {script_directory} && python bot.py'

subprocess.call(run_command, shell=True)
