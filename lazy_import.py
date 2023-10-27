import os
import importlib


module_directory = 'extractor'

imported_modules = {}

sub_directories = [d for d in os.listdir(module_directory) if os.path.isdir(os.path.join(module_directory, d))]

for subdir in sub_directories:
    module_files = [f for f in os.listdir(os.path.join(module_directory, subdir)) if f.endswith('.py')]

    for module_file in module_files:
        module_name = os.path.splitext(module_file)[0]
        module_path = f"{module_directory}.{subdir}.{module_name}"
        module = importlib.import_module(module_path)

        # print(f"Module name: {module_name} from {subdir}")
        imported_modules[module_name] = module