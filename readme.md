## Disclaimer
This project is aimed for getting images easily from korean sites in which the images are publicly available and not behind any paywall or login. This project is not intended for piracy or any other illegal activities in any way. All images this project downloads can be downloaded manually without this project by interacting with the website page. Any illegal activities done with this project is not the responsibility of the author.

## Table of Contents
* [Prerequisite](#prerequisite)
* [Usage](#usage)
* [Options](#options)
* [Supported Sites](#supported-sites)
* [Issues](#issues)
* [FAQ](#faq)

## Supported Sites

| Site Name | Site URL | Supported | Media Type |
| :--- | :--- | :---: | :---: |
| Cosmopolitan Korea | https://www.cosmopolitan.co.kr/ | Post Page | Image |
| Dazed Korea | https://www.dazedkorea.com/ | Post Page | Image |
| Dispatch (디스패치) | https://www.dispatch.co.kr/category/photos | Post Page | Image |
| Elle Korea | https://www.elle.co.kr/ | Post Page | Image |
| Esquire Korea | https://www.esquirekorea.co.kr/ | Post Page | Image |
| Harper's Bazaar Korea | https://www.harpersbazaar.co.kr/ | Post Page | Image |
| iMBC News | https://enews.imbc.com/ | Post Page | Image |
| JTBC TV | https://tv.jtbc.co.kr/ | Post Page | Image |
| K odyssey | https://k-odyssey.com/ | Post Page | Image |
| L'Officiel Korea | https://www.lofficielkorea.com/ | Post Page | Image |
| L'Officiel Singapore | https://www.lofficielsingapore.com/ | Post Page | Image |
| Marie Claire Korea | https://www.marieclairekorea.com/ | Post Page | Image |
| MBC PR (MBC와 함께) | https://with.mbc.co.kr/m/pr/photo/view.html | Post Page | Image |
| Nataliemu | https://nataliemu.com/ | Post Page | Image |
| Naver Posts (Naver 포스트) | https://post.naver.com/ | [Post Page](https://post.naver.com/viewer/postView.naver?volumeNo=35887849&memberNo=25831870), [Search Result](https://post.naver.com/search/authorPost.naver?keyword=%EC%95%84%EC%9D%B4%EB%B8%8C&memberNo=25831870), [Series List](https://post.naver.com/series.naver?memberNo=25831870), [Series Page](https://post.naver.com/my/series/detail.naver?seriesNo=671644&memberNo=25831870), [Main Page](https://post.naver.com/my.naver?memberNo=25831870&navigationType=push) | Image |
| Naver News | https://news.naver.com/ | Post Page | Image |
| Newsjamm | https://newsjamm.co.kr/ | Post Page | Image |
| News1 | https://www.news1.kr/ | Post Page | Image |
| Newsen | https://www.newsen.com/news_photo_hd.php | Post Page | Image |
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

## Prerequisite
`python3` installed.

Run `pip3 install -r requirements.txt` to install dependencies

## Usage
```python3 krsite-dl [OPTIONS] URL [URL...]```

```python3 krsite-dl https://example.com -d ~/Pictures/```

```python3 krsite-dl -a ~/Pictures/list.txt -d ~/Pictures```

```python3 krsite-dl -ai ~/Pictures/imagelist.txt -d ~/Pictures```

## Options
```
-a                        Text file containing site urls
-ai                       Text file containing image urls
-d                        The destination path for the downloaded file
--no-windows-filenames    (default=False) krsite-dl will keep the original filenames of the images. This includes filenames that are not allowed in Windows OS.
```
```*supports on generic sites (not listed above) may and may not work*```

## Issues
```
Please make an issue if you encounter any problems or just want to get more sites supported.

Site Name: 
Site URL (preferably the post page):
```
## FAQ
#### Q: Why is the download speed so slow?
A: The download speed is limited by the site itself. You can try to use a VPN to get a better speed.

#### Q: Can I set a default download path?
A: Yes, you can set a default download path by editing the config.ini file. The config.ini file is located in the same directory as the krsite-dl file. You can also set the default download path by using the -d option.

#### Q: Can I download images from multiple sites at once?
A: Yes, you can download images from multiple sites at once by using the -a option. The -a option takes in a text file containing site urls. Each line in the text file should contain a site url. You can also use the -ai option to download images from multiple sites at once (But this isn't working right now). The -ai option takes in a text file containing image urls. Each line in the text file should contain an image url.

#### Q: Can I download images from a site that is not listed above?
A: Yes, you probably can. You can also make an issue if you want to get a site supported.
