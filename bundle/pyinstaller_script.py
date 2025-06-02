import os
import sys

import PyInstaller.__main__

# Go up one directory to the root where krsite_dl/ lives
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
ENTRY_POINT = os.path.join(ROOT_DIR, 'krsite_dl', '__main__.py')
HOOK_DIR = os.path.join(ROOT_DIR, 'krsite_dl', '__pyinstaller')
# ICON_PATH = os.path.join(ROOT_DIR, 'assets', 'icon.ico')  # if exists

def main():
    # Ensure the script is run from the correct directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    # Define the PyInstaller command
    PyInstaller.__main__.run([
        ENTRY_POINT,
        '--name=krsite-dl',
        '--onedir',
        '--console',
        # f'--icon={ICON_PATH}',
        '--upx-exclude=vcruntime140.dll,'
        '--clean',
        '--distpath=dist',
        '--workpath=build',
        f'--additional-hooks-dir={HOOK_DIR}',
    ])
    print("PyInstaller build completed successfully.")

if __name__ == '__main__':
    main()
    sys.exit(0)