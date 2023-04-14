## Supported Sites
### 1. Naver Posts (Naver 포스트) https://post.naver.com/navigator.naver
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

### 2. Dispatch https://www.dispatch.co.kr/category/photos
* Post Page
```https://www.dispatch.co.kr/2239272```

### 3. iMBC News https://enews.imbc.com/
* Post Page
```https://enews.imbc.com/News/RetrieveNewsInfo/371280```

### 4. MBC PR (MBC와 함께) https://with.mbc.co.kr/pr/photo/
* Post Page
```https://with.mbc.co.kr/m/pr/photo/view.html?idx=56198&page=5&keyword=```

### 5. Newsjamm https://newsjamm.co.kr/
* Post Page
```https://newsjamm.co.kr/contents/642e7084129f6c0973201626```

### 6. OSEN

### 7. SBS
* Post Page
```https://programs.sbs.co.kr/special/pdnote/board/65942?search_option=title&search_keyword=%EC%95%84%EC%9D%B4%EB%B8%8C&cmd=multi_list&board_code=inkigayo_pt01&board_no=437548```


## Usage
```python3 krsite-dl [OPTIONS] URL [URL...]```

## Options
```
-a                        Text file containing site urls
-ai                       Text file containing image urls
-d                        The destination path for the downloaded file
--no-windows-filenames    By default krsite-dl will remove characters that are not allowed in Windows filenames. This option will disable that.
```
> *supports on generic sites (not listed above) may and may not work*