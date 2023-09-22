import requests
from bs4 import BeautifulSoup

def from_generic(hd, loc, folder_name):
    r = requests.get(hd)
    soup = BeautifulSoup(r.text, 'html.parser')
    img_list = []

    for item in soup.findAll('img'):
        img_list.append(item.get('src'))
    
    print("Found %s image(s)" % len(img_list))

    from down.directory import DirectoryHandler

    DirectoryHandler().handle_directory(img_list, None, None, None, loc, folder_name)