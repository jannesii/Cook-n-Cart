import os
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s"
)

def main():
    # 1) Grab the Windows Local AppData folder
    local_appdata = os.getenv("LOCALAPPDATA")
    if not local_appdata:
        logging.error("LOCALAPPDATA environment variable is not set.")
        return

    # 2) Compute where Python is installed
    python_home = os.path.join(local_appdata, "Programs", "Python", "Python311")
    if not os.path.isdir(python_home):
        logging.error("Expected Python install not found at %s", python_home)
        return

    # 3) Build the new pyenv.cfg content
    venv_dir = os.path.join(os.getcwd(), ".venv")
    cfg_content = f"""home = {python_home}
include-system-site-packages = false
version = 3.11.9
executable = {python_home}\\python.exe
command = {python_home}\\python.exe -m venv {venv_dir}
"""

    # 4) Write it out
    cfg_path = os.path.join(venv_dir, "pyvenv.cfg")
    with open(cfg_path, "w", encoding="utf-8") as f:
        f.write(cfg_content)

    logging.info("Wrote pyvenv.cfg at %s", cfg_path)

if __name__ == "__main__":
    main()
