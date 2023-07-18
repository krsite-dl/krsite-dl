import down.directory as dir

def from_direct(url):
    print("Url: %s" % url)
    title = url.split('/')[-1]
    dir.dir_handler_alt(url, title)