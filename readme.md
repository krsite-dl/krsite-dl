If you like this project, please consider giving it a star! Thanks!

## Table of Contents
* [Prerequisite](#prerequisite)
* [Usage](#usage)
* [Options](#options)
* [Supported Sites](#supported-sites)
* [Issues](#issues)
* [FAQ](#faq)
* [Disclaimer](#disclaimer)

## Prerequisite
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
-d                        The destination path for the downloaded file (unnecessary if config.ini is setup unless you want to override the default download path)
--no-windows-filenames    (default=False) By default krsite-dl will remove characters that are not allowed in Windows filenames. This option will disable that.
```

## Supported Sites

| Site Name | Site URL | Supported | Media Type | Requires Selenium |
| :--- | :--- | :---: | :---: | :---: |
| Cosmopolitan Korea | https://www.cosmopolitan.co.kr/ | Post Page | Image |
| Dazed Korea | https://www.dazedkorea.com/ | Post Page | Image |
| Dispatch (디스패치) | https://www.dispatch.co.kr/category/photos | Post Page | Image 
| Elle Korea | https://www.elle.co.kr/ | Post Page | Image | |
| Esquire Korea | https://www.esquirekorea.co.kr/ | Post Page | Image | |
| Harper's Bazaar Korea | https://www.harpersbazaar.co.kr/ | Post Page | Image |
| iMBC News | https://enews.imbc.com/ | Post Page | Image | |
| JTBC TV | https://tv.jtbc.co.kr/ | Post Page | Image | |
| K odyssey | https://k-odyssey.com/ | Post Page | Image | |
| L'Officiel Korea | https://www.lofficielkorea.com/ | Post Page | Image | Yes |
| L'Officiel Singapore | https://www.lofficielsingapore.com/ | Post Page | Image | Yes |
| Marie Claire Korea | https://www.marieclairekorea.com/ | Post Page | Image |
| MBC PR (MBC와 함께) | https://with.mbc.co.kr/m/pr/photo/view.html | Post Page | Image | Yes |
| Nataliemu | https://nataliemu.com/ | Post Page | Image | 
| Naver Posts (Naver 포스트) | https://post.naver.com/ | [Post Page](https://post.naver.com/viewer/postView.naver?volumeNo=35887849&memberNo=25831870), [Search Result](https://post.naver.com/search/authorPost.naver?keyword=%EC%95%84%EC%9D%B4%EB%B8%8C&memberNo=25831870), [Series List](https://post.naver.com/series.naver?memberNo=25831870), [Series Page](https://post.naver.com/my/series/detail.naver?seriesNo=671644&memberNo=25831870), [Main Page](https://post.naver.com/my.naver?memberNo=25831870&navigationType=push) | Image | Yes |
| Naver News | https://news.naver.com/ | Post Page | Image |
| Newsjamm | https://newsjamm.co.kr/ | Post Page | Image |
| News1 | https://www.news1.kr/ | Post Page | Image | 
| Newsen | https://www.newsen.com/news_photo_hd.php | Post Page | Image | Yes |
| OSEN | https://osen.mt.co.kr/ | Post Page | Image |
| SBS Program | https://programs.sbs.co.kr/ | Post Page | Image |
| SBS News | https://news.sbs.co.kr/ | Post Page | Image |
| Topstarnews | https://www.topstarnews.net/ | Post Page, Search Result Page, [HD Posts Page](https://www.topstarnews.net/news/articleList.html?sc_article_type=C&view_type=tm) | Image |
| TV Report (TV리포트) | https://tvreport.co.kr/ | Post Page | Image |
| TV JTBC | https://tv.jtbc.co.kr/ | Post Page | Image |
| Vivi | https://www.vivi.tv/ | 🚧 | Image |
| Vogue Korea | https://www.vogue.co.kr/ | Post Page | Image |
| W Korea | https://www.wkorea.com/ | Post Page | Image |
| Generic Sites | Any Sites not listed above | ? | Image |

## Issues
> [!NOTE]
> Please make an issue if you encounter any problems or just want to get more sites supported.
>
> Site Name: www.example.com
>
> Site URL (preferably the post page): www.example.com/post/1234

## FAQ
#### Q: Why is the download speed so slow?
A: The download speed is limited by the site itself. You can try to use a VPN to get a better speed.

#### Q: Can I set a default download path?
A: Yes, you can set a default download path by editing the config.ini file. The config.ini file is located in the same directory as the krsite-dl file. You can also set the default download path by using the -d option.

#### Q: Can I download images from multiple sites at once?
A: Yes, you can download images from multiple sites at once by using the -a option. The -a option takes in a text file containing site urls. Each line in the text file should contain a site url. You can also use the -ai option to download images from multiple sites at once (But this isn't working right now). The -ai option takes in a text file containing image urls. Each line in the text file should contain an image url.

#### Q: Can I download images from a site that is not listed above?
A: Yes, you probably can. You can also make an issue if you want to get a site supported.


# Disclaimer

This project is intended solely for the purpose of easily obtaining images from Korean websites where the images are publicly available and not behind any paywall or login. It is essential to understand and adhere to the following:

1. **Purpose**: The primary aim of this project is to provide a convenient means to access publicly available images on Korean websites. It is not intended for engaging in piracy or any illegal activities in any way.

2. **Legal Use**: You must use this project in strict accordance with all applicable laws and regulations. Any illegal activities or misuse of this project are the sole responsibility of the user and not the author.

3. **Accessibility**: All images obtained using this project can also be acquired manually by interacting with the website's pages. This project merely automates the process for ease of access.

4. **User Responsibility**: Reusing, editing, sharing, sending, or redistributing images downloaded using this project is at your own risk. The author disclaims any liability for any consequences or legal issues that may arise from such actions.

5. **Author's Non-Involvement**: The author of this project (hereinafter referred to as "the author") disclaims any involvement in, or responsibility for, any actions or activities undertaken by users of this project that may infringe upon copyrights, terms of service, or any other legal obligations.

6. **Disclaimer of Liability**: The author provides no warranties or guarantees regarding the functionality, accuracy, or fitness for a particular purpose of this project. Users employ this project at their own risk.

7. **Support**: While the author may offer limited support for this project, there is no obligation to do so. Support is offered at the author's discretion.

By using this project, you acknowledge and agree to abide by these terms and conditions. If you do not agree with these terms, you should refrain from using this project.

Please ensure that you use this project responsibly and in compliance with all applicable laws and the terms of service of the websites accessed. The author disclaims any responsibility for any misuse or violations of third-party websites' terms of service or policies.