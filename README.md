If you like this project, please consider giving it a star! Thanks!

## Table of Contents
* [Guides & Installation](#Guides--Installation)
* [Usage](#usage)
* [Options](#options)
* [Supported Sites](./supported.md)
* [Issues](#issues)
* [Disclaimer](#disclaimer)

## Guides & Installation
> [!IMPORTANT]
> 1. Make sure you have `python3` at least version 3.6 installed and executeable in your system's PATH.
>
> 2. Run `pip3 install -r requirements.txt` to install dependencies
> 
> 3. There are some sites that requires selenium. User must have [chrome](https://www.google.com/chrome/) and [chromedriver](https://chromedriver.chromium.org/downloads) installed and executeable. The list of sites can be found [here](#supported-sites).

> [!NOTE]
> To update the script, you need to pull this repository again. You can also run `git pull` if you have git installed.
> Make sure to run another `pip install -r requirements.txt` to install any new dependencies.
> In case you ran into a `chromedriver` error, you need to update your `chromedriver`. You can download the latest chrome driver [here](https://chromedriver.chromium.org/downloads).

## Usage
User can add `krsite-dl.conf` file to set default download path. You can put the file in the following locations for automatic detection.

### Windows

`%APPDATA%\krsite-dl\krsite-dl.conf`

`%USERPROFILE%\krsite-dl\krsite-dl.conf`

`%USERPROFILE%\krsite-dl.conf`

### Linux

`/etc/krsite-dl.conf`

`~/.config/krsite-dl/krsite-dl.conf`

`~/krsite-dl.conf`


> [!NOTE]
>
> The `krsite-dl.conf` file should contain the following:
> ```
> [Settings]
>
> base_dir = <path>
> ```

### Basic Usage
```python3 krsite_dl.py [-h] [-c CONFIG] [-a A] [-d DESTINATION] [-s] [--no-windows-filenames] [url ...]```

`python3 krsite-dl https://example.com/1/`

`python3 krsite-dl https://example.com/1/ https//example.com/2/`

**Download by specifying the download path**

Alternatively, you can specify the download path by default by using krsite-dl.config file.

```python3 krsite-dl https://example.com -d ~/Pictures/```


**Downloading from multiple sites in a text file**

```python3 krsite-dl -a ~/Pictures/list.txt -d ~/Pictures```

### Selecting an image to download

**This will prompt you a list of images to download**

```python3 krsite-dl https://example.com -s```


## Options
```
usage: krsite_dl.py [-h] [-c CONFIG] [-a A] [-d DESTINATION] [-s] [--no-windows-filenames] [url ...]

positional arguments:
  url                   valid news/blog url

options:
  -h, --help            show this help message and exit

utility:
  -c CONFIG, --config CONFIG
                        File path to your config file
  -a A                  Text file containing site urls
  -d DESTINATION, --destination DESTINATION
                        The destination path for the downloaded file (unnecessary if you have `krsite-dl.config` unless you want
                        to override the default download path)
  -s, --select          Select which images to download from the list of images gathered from each url. You probably not wanna
                        use this if you're downloading multiple site URLs at once cause it will prompt you for each url.

misc:
  --no-windows-filenames
                        (default=False) krsite-dl will keep the original filenames of the images. This includes filenames that
                        are not allowed in Windows OS.
```

## Issues
> [!NOTE]
> Please make an issue if you encounter any problems or just want to get more sites supported.
>
> Site Name: www.example.com
>
> Site URL (preferably the post page): www.example.com/post/1234


# Disclaimer

This program is solely intended for the purpose of easily obtaining images from Korean websites where the images are publicly available and not behind any paywall or login. By using this program, you agree that you are responsible for your own actions. The author and maintainer of this program is not responsible for any loss or damage caused by the use of this program.