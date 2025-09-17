[![PyPI - Version](https://img.shields.io/pypi/v/krsite-dl?label=PyPI)](https://pypi.org/project/krsite-dl/)
![Pepy Total Downloads](https://img.shields.io/pepy/dt/krsite-dl?label=Downloads)
[![GitHub Release Date](https://img.shields.io/github/release-date/krsite-dl/krsite-dl?label=Release%20Date)]()
[![Visitors](https://visitor-badge.laobi.icu/badge?page_id=krsite-dl.krsite-dl)](https://github.com/krsite-dl/krsite-dl)
[![Forks](https://img.shields.io/github/forks/krsite-dl/krsite-dl)]()
[![Stars](https://img.shields.io/github/stars/krsite-dl/krsite-dl)]()
[![Static Badge](https://img.shields.io/badge/-Supported_Sites-brightgreen?link=https%3A%2F%2Fgithub.com%2Fkrsite-dl%2Fkrsite-dl%2Fblob%2Fmaster%2Fsupported.md)
](supported.md)
<br>
[![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/krsite-dl/krsite-dl/release.yml?label=CI)]()
[![Release branch (master)](https://github.com/krsite-dl/krsite-dl/actions/workflows/release.yml/badge.svg)](https://github.com/krsite-dl/krsite-dl/actions/workflows/release.yml)
[![CodeQL](https://github.com/krsite-dl/krsite-dl/actions/workflows/github-code-scanning/codeql/badge.svg?branch=master)](https://github.com/krsite-dl/krsite-dl) [![Dependency Review](https://github.com/krsite-dl/krsite-dl/actions/workflows/dependency-review.yml/badge.svg)](https://github.com/krsite-dl/krsite-dl)
[![License](https://img.shields.io/github/license/krsite-dl/krsite-dl?label=License)](https://github.com/krsite-dl/krsite-dl)

## Table of Contents

- [Guides & Installation](#Guides--Installation)
  - [Installing with pip](#installing-with-pip)
  - [Pulling from GitHub](#pulling-from-github)
  - [Installing from source](#installing-from-source)
- [Usage](#usage)
  - [Configuration](#configuration)
  - [Basic Usage](#basic-usage)
  - [Selecting an image to download](#selecting-an-image-to-download)
- [Options](#options)
- [Supported Sites](./supported.md)
- [Issues](#issues)
- [Disclaimer](#disclaimer)

## Guides & Installation

### Installing with pip

You can install `krsite-dl` using pip. This is the recommended way to install the script.

```bash
pip install krsite-dl
```

### Pulling from GitHub

You can also install `krsite-dl` by pulling the latest code from GitHub.

```bash
git clone -b master git@github.com:krsite-dl/krsite-dl.git
```

<b>Or</b>

Download the latest release from [releases](https://github.com/krsite-dl/krsite-dl/releases/latest)

Then run the following command to install dependencies:

```bash
pip3 install -r requirements.txt
```

## Usage

### Configuration

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

`krsite-dl [-h] [-c CONFIG] [-a A] [-d DESTINATION] [-s] [-v] [--no-windows-filenames] [url ...]`

`krsite-dl https://example.com/1/`

`krsite-dl https://example.com/1/ https//example.com/2/`

> [!NOTE]
>
> If you use the source code, you can run the script directly with `python3 -m krsite_dl.py` or `python -m krsite_dl.py`.

**Download by specifying the download path**

Alternatively, you can specify the download path by default by using krsite-dl.config file.

`krsite-dl https://example.com -d ~/Pictures/`

**Download by specifying the config path**

`krsite-dl -c ~/krsite-dl.conf https://example.com`

**Downloading from multiple sites in a text file**

`krsite-dl -a ~/Pictures/list.txt -d ~/Pictures`

### Selecting an image to download

**This will prompt you a list of images to download**

`krsite-dl https://example.com -s`

## Issues

> [!NOTE]
> Please make an issue if you encounter any problems or just want to get more sites supported.
>
> Site Name: www.example.com
>
> Site URL (preferably the post page): www.example.com/post/1234

# Disclaimer

This program is solely intended for the purpose of easily obtaining images from Korean websites where the images are publicly available and not behind any paywall or login. By using this program, you agree that you are responsible for your own actions and your action afterwards. The author and maintainer of this program is not responsible for any loss or damage caused by the use of this program.
