If you like this project, please consider giving it a star! Thanks!

## Table of Contents
* [Guides & Installation](#Guides--Installation)
* [Usage](#usage)
* [Options](#options)
* [Supported Sites](#supported-sites)
* [Issues](#issues)
* [FAQ](#faq)
* [Disclaimer](#disclaimer)

## Guides & Installation
> [!IMPORTANT]
> 1. Make sure you have `aria2c` installed and executeable in your system's PATH.
>
>   Install `aria2c` from https://github.com/aria2/aria2
>
> 2. Make sure you have `python3` at least version 3.6 installed and executeable in your system's PATH.
>
> 3. Run `pip3 install -r requirements.txt` to install dependencies
> 
> 4. There are some sites that requires selenium. User must have [chrome](https://www.google.com/chrome/) and [chromedriver](https://chromedriver.chromium.org/downloads) installed and executeable. The list of sites can be found [here](#supported-sites).

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

```python3 krsite-dl [OPTIONS] URL [URL...]```

```python3 krsite-dl https://example.com -d ~/Pictures/```

```python3 krsite-dl -a ~/Pictures/list.txt -d ~/Pictures```

```python3 krsite-dl -ai ~/Pictures/imagelist.txt -d ~/Pictures```

## Options
```
-a                        Text file containing site urls
-ai                       Text file containing image urls
-d                        The destination path for the downloaded file (unnecessary if you have `krsite-dl.config` unless you want to override the default download path)
--no-windows-filenames    (default=False) krsite-dl will keep the original filenames of the images. This includes filenames that are not allowed in Windows OS.
```

## Supported Sites

| Site Name | Site URL | Supported | Media Type | Requires Selenium |
| :--- | :--- | :---: | :---: | :---: |
| Cosmopolitan Korea | https://www.cosmopolitan.co.kr/ | Post Page | Image |
| Dazed Korea | https://www.dazedkorea.com/ | Post Page | Image |
| Dispatch (디스패치) | https://www.dispatch.co.kr/category/photos | Post Page | Image 
| Elle Korea | https://www.elle.co.kr/ | Post Page | Image | |
| Esquire Korea | https://www.esquirekorea.co.kr/ | Post Page | Image | |
| Genie Music | https://www.genie.co.kr/ | [Artist Page](https://www.genie.co.kr/detail/artistInfo?xxnm=81271496) | Image |
| Harper's Bazaar Korea | https://www.harpersbazaar.co.kr/ | Post Page | Image |
| iMBC News | https://enews.imbc.com/ | Post Page | Image | |
| JTBC TV | https://tv.jtbc.co.kr/ | Post Page | Image | |
| K odyssey | https://k-odyssey.com/ | Post Page | Image | |
| L'Officiel Korea | https://www.lofficielkorea.com/ | Post Page | Image | Yes |
| L'Officiel Singapore | https://www.lofficielsingapore.com/ | Post Page | Image | Yes |
| Marie Claire Korea | https://www.marieclairekorea.com/ | Post Page | Image |
| MBC PR (MBC와 함께) | https://with.mbc.co.kr/m/pr/photo/view.html | Post Page | Image | Yes |
| Melon | https://www.melon.com/ | [Artist Page](https://www.melon.com/artist/photo.htm?artistId=3055146) | Image |
| Nataliemu | https://nataliemu.com/ | Post Page | Image | 
| Naver Posts (Naver 포스트) | https://post.naver.com/ | [Post Page](https://post.naver.com/viewer/postView.naver?volumeNo=35887849&memberNo=25831870), [Search Result](https://post.naver.com/search/authorPost.naver?keyword=%EC%95%84%EC%9D%B4%EB%B8%8C&memberNo=25831870), [Series List](https://post.naver.com/series.naver?memberNo=25831870), [Series Page](https://post.naver.com/my/series/detail.naver?seriesNo=671644&memberNo=25831870), [Main Page](https://post.naver.com/my.naver?memberNo=25831870&navigationType=push) | Image | Yes |
| Naver News | https://news.naver.com/ | Post Page | Image |
| Newsjamm | https://newsjamm.co.kr/ | Post Page | Image |
| News1 | https://www.news1.kr/ | Post Page | 🚧 | 
| Newsen | https://www.newsen.com/news_photo_hd.php | Post Page | Image | Yes |
| Non-no Korea | https://www.nonno.hpplus.jp/ | Post Page | Image |
| OSEN | https://osen.mt.co.kr/ | Post Page | Image |
| SBS Program | https://programs.sbs.co.kr/ | Post Page | Image |
| SBS News | https://news.sbs.co.kr/ | Post Page | Image |
| SBS KPOP | https://sbskpop.kr/ | Post Page | Image |
| Topstarnews | https://www.topstarnews.net/ | Post Page, Search Result Page, [HD Posts Page](https://www.topstarnews.net/news/articleList.html?sc_article_type=C&view_type=tm) | Image |
| TV Report (TV리포트) | https://tvreport.co.kr/ | Post Page | Image |
| TV JTBC | https://tv.jtbc.co.kr/ | Post Page | Image |
| Vivi | https://www.vivi.tv/ | Post Page | Image |
| Vogue Korea | https://www.vogue.co.kr/ | Post Page | Image |
| W Korea | https://www.wkorea.com/ | Post Page | Image |

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
A: Yes, you can download images from multiple sites at once by using the -a option. The -a option takes in a text file containing site urls. Each line in the text file should contain a site url. You can also use the -ai option to download images from multiple sites at once (But this isn't working right now). The -ai option takes in a text file containing image urls. Each line in the text file should contain an image url.

#### Q: Can I download images from a site that is not listed above?
A: No, you can make request for the site to be supported. Make an issues and then feature request.


# Disclaimer

This project is intended solely for the purpose of easily obtaining images from Korean websites where the images are publicly available and not behind any paywall or login. Any commercial use of this project is strictly prohibited. By using this project, you agree that you are responsible for your own actions. The author of this project is not responsible for any misuse of the information provided by this project.