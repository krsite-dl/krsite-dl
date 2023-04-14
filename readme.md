## Table of Contents
* [Supported Sites](#supported-sites)
    * [Naver Posts (Naver 포스트)](#naver-posts-naver-포스트)
    * [Naver News](#naver-news)
    * [Dispatch (디스패치)](#dispatch-디스패치)
    * [iMBC News](#imbc-news)
    * [MBC PR (MBC와 함께)](#mbc-pr-mbc와-함께)
    * [Newsjamm](#newsjamm)
    * [OSEN](#osen)
    * [SBS Program](#sbs-program)
    * [SBS News](#sbs-news)
    * [TV Report (TV리포트)](#tv-report-tv리포트)
    * [K odyssey](#k-odyssey)
* [Usage](#usage)
* [Options](#options)

## Supported Sites
### Naver Posts (Naver 포스트)
```https://post.naver.com/```
* Main Page
```https://post.naver.com/my.naver?memberNo=24876555```
* Search Result
```https://post.naver.com/search/authorPost.naver?keyword=%EC%95%84%EC%9D%B4%EC%A6%88%EC%9B%90&memberNo=24876555```
* Series List
```https://post.naver.com/series.naver?memberNo=24876555```
* Series Page
```https://post.naver.com/my/series/detail.naver?memberNo=24876555&seriesNo=598640```
* Post Page
```https://post.naver.com/viewer/postView.naver?volumeNo=28559893&memberNo=24876555&navigationType=push```

### Naver News
### Dispatch (디스패치)
```https://www.dispatch.co.kr/category/photos```
* Post Page
```https://www.dispatch.co.kr/2239272```

### iMBC News
```https://enews.imbc.com/```
* Post Page
```https://enews.imbc.com/News/RetrieveNewsInfo/371280```

### MBC PR (MBC와 함께)
```https://with.mbc.co.kr/pr/photo/```
* Post Page
```https://with.mbc.co.kr/m/pr/photo/view.html?idx=56198&page=5&keyword=```

### Newsjamm
```https://newsjamm.co.kr/```
* Post Page
```https://newsjamm.co.kr/contents/642e7084129f6c0973201626```

### OSEN
```https://osen.mt.co.kr/```
* Post Page
```https://osen.mt.co.kr/article/G1111909432```

### SBS Program
```https://programs.sbs.co.kr/```
* Post Page
```https://programs.sbs.co.kr/special/pdnote/board/65942?search_option=title&search_keyword=%EC%95%84%EC%9D%B4%EB%B8%8C&cmd=multi_list&board_code=inkigayo_pt01&board_no=437548```

### SBS News
```https://news.sbs.co.kr/```
* Post Page
```https://ent.sbs.co.kr/news/article.do?article_id=E10010268907&plink=ORI&cooper=NAVER```

### TV Report (TV리포트)
```https://tvreport.co.kr/```
* Post Page
```https://tvreport.co.kr/star/article/718199/```

### K odyssey
```https://k-odyssey.com/```
* Post Page
```https://k-odyssey.com/news/newsview.php?ncode=1065598383621554```

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
--no-windows-filenames    By default krsite-dl will remove characters that are not allowed in Windows filenames. This option will disable that.
```
```*supports on generic sites (not listed above) may and may not work*```