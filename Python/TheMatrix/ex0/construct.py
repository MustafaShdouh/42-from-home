import sys
import os
import site

enable_user_site: bool | None = site.ENABLE_USER_SITE
is_virtual: bool = sys.prefix != sys.base_prefix

if not is_virtual:
    print("MATRIX STATUS: You're still plugged in\n")
    print(f"Current Python: {sys.executable}")
    print("Virtual Environment: None detected\n")
    print("WARNING: You're in the global environment!")
    print("The machines can see everything you install.\n")
    print("To enter the construct, run:")
    print("python -m venv matrix_env")
    print("source matrix_env/bin/activate # On Unix")
    print("matrix_env\\Scripts\\activate # On Windows\n")
    print("Then run this program again.")

if is_virtual:
    if not enable_user_site:
        venv_path: str = sys.prefix
        venv_name: str = os.path.basename(venv_path)
        packages: str = site.getsitepackages()[0]
        print("MATRIX STATUS: Welcome to the construct\n")
        print(f"Current Python: {sys.executable}")
        print(f"Virtual Environment: {venv_name}")
        print(f"Environment Path: {venv_path}\n")
        print("SUCCESS: You're in an isolated environment!")
        print("Safe to install packages without"
              " affecting the global system.\n")
        print(f"Package installation path: {packages}")
    else:
        print("You are in a virtual environment, but you are "
              "using global corrupted packages!")
