from PyInstaller.utils.hooks import collect_submodules, collect_data_files

def get_hidden_imports():
    yield from collect_submodules('krsite_dl')
    yield from collect_submodules('krsite_dl.extractor')



hiddenimports = list(get_hidden_imports())
datas = collect_data_files('krsite_dl', 'krsite_dl') + collect_data_files('krsite_dl.extractor', 'krsite_dl.extractor')

print("PyInstaller hook for krsite_dl:")
print(f"Hidden imports: {hiddenimports}")
print(f"Data files: {datas}")