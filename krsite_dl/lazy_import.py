import os
import sys
import importlib

def get_application_root_path():
    """
    Determines the correct root path for the application,
    whether running as a script or as a PyInstaller bundle.
    """
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        # Running in a PyInstaller bundle (frozen)
        # sys._MEIPASS is the path to the temporary folder where PyInstaller unpacks the app
        return sys._MEIPASS
    else:
        return os.path.dirname(os.path.abspath(__file__))

# Get the true root path of the application (where 'extractor' will be)
_APP_ROOT_PATH = get_application_root_path()

# The NAME of the directory containing modules (for import statements)
MODULE_ROOT_DIR_NAME = 'extractor'

# The actual FILE SYSTEM PATH to this directory (for os.listdir, os.path.join etc.)
module_directory_fs_path = os.path.join(_APP_ROOT_PATH, MODULE_ROOT_DIR_NAME)

imported_modules = {}

if not os.path.isdir(module_directory_fs_path):
    raise FileNotFoundError(
        f"The module directory '{MODULE_ROOT_DIR_NAME}' was not found at '{module_directory_fs_path}'. "
        f"Ensure it's correctly bundled by PyInstaller (using 'datas' in .spec) "
        f"and that all necessary __init__.py files are present."
    )

# Add the application root path to sys.path.
# This ensures that importlib.import_module can find the 'extractor' package
# when the application is bundled. PyInstaller usually handles _MEIPASS,
# but being explicit can prevent issues.
if _APP_ROOT_PATH not in sys.path:
    sys.path.insert(0, _APP_ROOT_PATH)

sub_directories = [d for d in os.listdir(module_directory_fs_path)
                   if os.path.isdir(os.path.join(module_directory_fs_path, d))]

for subdir_name in sub_directories:
    current_subdir_fs_path = os.path.join(module_directory_fs_path, subdir_name)
    module_files = [f for f in os.listdir(current_subdir_fs_path) if f.endswith('.py')]

    for module_file_name in module_files:
        simple_module_name = os.path.splitext(module_file_name)[0]

        # Construct the full import path, e.g., "extractor.jp.nonno"
        # MODULE_ROOT_DIR_NAME is 'extractor'
        module_import_path = f"{MODULE_ROOT_DIR_NAME}.{subdir_name}.{simple_module_name}"

        try:
            module = importlib.import_module(module_import_path)
            # Storing by simple name. Consider if a more qualified name is needed
            # if simple_module_names can collide across subdirectories.
            imported_modules[simple_module_name] = module
        except ImportError as e:
            print(f"Failed to import module '{module_import_path}': {e}")
            print(f"  Search path (sys.path): {sys.path}")
            print(f"  Please ensure that '{MODULE_ROOT_DIR_NAME}/' and '{MODULE_ROOT_DIR_NAME}/{subdir_name}/' "
                  f"contain an '__init__.py' file if they are intended as packages.")
