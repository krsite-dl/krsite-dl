[![Visitors](https://visitor-badge.laobi.icu/badge?page_id=krsite-dl.krsite-dl)](https://github.com/krsite-dl/krsite-dl)
[![Stars](https://img.shields.io/github/stars/krsite-dl/krsite-dl)]()
[![Forks](https://img.shields.io/github/forks/krsite-dl/krsite-dl)]()
<br>
[![CodeQL](https://github.com/krsite-dl/krsite-dl/actions/workflows/github-code-scanning/codeql/badge.svg?branch=master)](https://github.com/krsite-dl/krsite-dl) [![Dependency Review](https://github.com/krsite-dl/krsite-dl/actions/workflows/dependency-review.yml/badge.svg)](https://github.com/krsite-dl/krsite-dl)
[![License](https://img.shields.io/github/license/krsite-dl/krsite-dl)](https://github.com/krsite-dl/krsite-dl)

## Table of Contents

- [Guides & Installation](#Guides--Installation)
- [Usage](#usage)
- [Options](#options)
- [Supported Sites](./supported.md)
- [Issues](#issues)
- [Disclaimer](#disclaimer)

## Guides & Installation

> [!IMPORTANT]
>
> 1. Make sure you have `python3` at least version 3.7 installed and executeable in your system's PATH.
>
> 2. Clone this repository `git clone -b master git@github.com:krsite-dl/krsite-dl.git`
>
> 3. Run `pip3 install -r requirements.txt` to install dependencies

> [!NOTE]
> To update the script, you need to pull this repository again. You can also run `git pull` if you have git installed.
> Make sure to run another `pip install -r requirements.txt` to install any new dependencies.

## Usage

User can add `krsite-dl.conf` file to set default download path. You can put the file in the following locations for automatic detection. This will get overridden by config path specified by `-c` option.

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
>
> ```
> [Settings]
>
> base_dir = <path>
> ```

### Basic Usage

`python3 krsite_dl.py [-h] [-c CONFIG] [-a A] [-d DESTINATION] [-s] [-v] [--no-windows-filenames] [url ...]`

`python3 krsite-dl.py https://example.com/1/`

`python3 krsite-dl.py https://example.com/1/ https//example.com/2/`

**Download by specifying the download path**

Alternatively, you can specify the download path by default by using krsite-dl.config file.

`python3 krsite-dl.py https://example.com -d ~/Pictures/`

**Download by specifying the config path**

`python3 krsite-dl.py -c ~/krsite-dl.conf https://example.com`

**Downloading from multiple sites in a text file**

`python3 krsite-dl.py -a ~/Pictures/list.txt -d ~/Pictures`

### Selecting an image to download

**This will prompt you a list of images to download**

`python3 krsite-dl.py https://example.com -s`

## Options

```
usage: krsite_dl.py [-h] [-c CONFIG] [-a A] [-d DESTINATION] [-s] [-v] [--no-windows-filenames] [url ...]

positional arguments:
  url                   valid news/blog url

options:
  -h, --help            show this help message and exit

utility:
  -c CONFIG, --config CONFIG
                        File path to your config file
  -a A                  Text file containing site urls
  -d DESTINATION, --destination DESTINATION
                        The destination path for the downloaded file.
  -s, --select          Select which images to download from each url.
  -v, --verbose         Increase output verbosity

misc:
  --no-windows-filenames
                        (default=False) krsite-dl will not sanitize filenames
```

## Issues

> [!NOTE]
> Please make an issue if you encounter any problems or just want to get more sites supported.
>
> Site Name: www.example.com
>
> Site URL (preferably the post page): www.example.com/post/1234

# Disclaimer

This program is solely intended for the purpose of easily obtaining images from Korean websites where the images are publicly available and not behind any paywall or login. By using this program, you agree that you are responsible for your own actions and your action afterwards. The author and maintainer of this program is not responsible for any loss or damage caused by the use of this program.
