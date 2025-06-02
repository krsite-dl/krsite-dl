# from PyInstaller.utils.hooks import collect_submodules

# def get_hidden_imports():
#     yield ('krsite_dl.utils')
#     yield ('krsite_dl.extractor')

#     for module in ('krsite_dl.extractor',):
#         yield from collect_submodules(module)

# hidden_imports = list(get_hidden_imports())

# print(f"Hidden imports: {hidden_imports}")

from PyInstaller.utils.hooks import collect_submodules, collect_data_files

def get_hidden_imports():
    yield from collect_submodules('krsite_dl')
    yield from collect_submodules('krsite_dl.extractor')



hiddenimports = list(get_hidden_imports())
datas = collect_data_files('krsite_dl', 'krsite_dl') + collect_data_files('krsite_dl.extractor', 'krsite_dl.extractor')

print("PyInstaller hook for krsite_dl:")
print(f"Hidden imports: {hiddenimports}")
print(f"Data files: {datas}")