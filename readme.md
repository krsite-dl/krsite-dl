If you like this project, please consider giving it a star! Thanks!

## Table of Contents
* [Guides & Installation](#Guides--Installation)
* [Usage](#usage)
* [Options](#options)
* [Supported Sites](supported.md)
* [Issues](#issues)
* [FAQ](#faq)
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
User can add `krsite-dl.config` file to set default download path. The `krsite-dl.config` file is located in the same directory as the krsite-dl file.
> [!NOTE]
>
> The `krsite-dl.config` file should contain the following:
> ```
> [Settings]
>
> base_dir = /your/path/here
> ```

### Basic Usage
```python3 krsite-dl [OPTIONS] URL [URL...]```

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
-a                        Text file containing site urls
-ai                       Text file containing image urls
-d                        The destination path for the downloaded file (unnecessary if you have `krsite-dl.config` unless you want to override the default download path)
--no-windows-filenames    (default=False) krsite-dl will keep the original filenames of the images. This includes filenames that are not allowed in Windows OS.
-s                        Select which images to download from the list of images gathered from each url. You probably not wanna use this if you're downloading multiple site URLs at once cause it will prompt you for each url.
```

## Issues
> [!NOTE]
> Please make an issue if you encounter any problems or just want to get more sites supported.
>
> Site Name: www.example.com
>
> Site URL (preferably the post page): www.example.com/post/1234

## FAQ
#### Q: Why is the download speed so slow?
A: The download speed is limited by the site itself and your internet connection. You can try to use a VPN to get a better speed if necessary to avoid overseas rate limit.

#### Q: Can I set a default download path?
A: Yes, you can set a default download path by editing the config.ini file. The config.ini file is located in the same directory as the krsite-dl file. You can also set the default download path by using the -d option.

#### Q: Can I download images from multiple sites at once?
A: Yes, you can download images from multiple sites at once just by entering sites you want to download in one single command. Alternatively you can use the `-a` option if you wanna provide a text file containing site urls. 

#### Q: Can I download images from a site that is not listed above?
A: No, you can make request for the site to be supported. Make an issues and then feature request.


# Disclaimer

This project is intended solely for the purpose of easily obtaining images from Korean websites where the images are publicly available and not behind any paywall or login. Any commercial use of this project is strictly prohibited. By using this project, you agree that you are responsible for your own actions. The author of this project is not responsible for any misuse of the information provided by this project.