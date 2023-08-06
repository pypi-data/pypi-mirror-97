![Search Me](https://is.gd/search_me_logo)


# Search Me

Search in: **Google**, **Rambler**. Extract data from: **VK, Telegram, Instagram, YouTube, Twitter**

[![Version](https://img.shields.io/pypi/v/search-me.svg?style=flat-square&logo=appveyor)](https://pypi.org/project/search-me)
[![License](https://img.shields.io/pypi/l/search-me.svg?style=flat-square&logo=appveyor)](https://pypi.org/project/search-me)
[![Python](https://img.shields.io/pypi/pyversions/search-me.svg?style=flat-square&logo=appveyor)](https://pypi.org/project/search-me)
[![Status](https://img.shields.io/pypi/status/search-me.svg?style=flat-square&logo=appveyor)](https://pypi.org/project/search-me)
[![Downloads](https://img.shields.io/pypi/dm/search-me.svg?style=flat-square&logo=appveyor)](https://pypistats.org/packages/search-me)

## PRE-INSTALLING

- If you want to generate PDF documents (param *pdf_report*), setup [wkhtmltopdf](https://is.gd/html2pdf)
- If you want to download video from youtube (param *socials*), setup [youtube-dl](https://is.gd/youtube_dl)

## INSTALLING

```bash
pip install search-me
```

## USAGE

### Imports

```python
from search_me import Google, Rambler
```

### Init search engine

```python
searcher = Google()
searcher = Rambler()
```

Parameters:

- *results*: Number of search results on page (*default: 10*)
- *retry*: Number of retries for one query (*default: 10*)
- *socials*: Tuple with names of social nets (*default: ("vk", "instagram", "telegram", "twitter", "youtube")*)
- *pdf_report*: Export searched data to pdf-documents (*default: False*)
- *pdf_timeout*: Waiting time in seconds for create pdf-document (*default: 30*)
- *cache*: Caching searched data after each search query in pkl file (*default: True*)
- *sleep_min*: Minimum time in seconds to sleep after each query (*default: 0.0*)
- *sleep_max*: Maximum time in seconds to sleep after each query (*default: 1.5*)

### Start search

```python
searched = searcher.search(items=["query 1", "query 2"])
```

### Look results in table

```python
searcher.show(results=searched)
```

### Apply social processing

```python
searched_social = searcher.use_social(searched=searched)
```

Parameters:

- *posts_limit*: Number of posts for VK, Telegram, Twitter, Youtube (*default: 10*)
- *export_data*: Export data about posts in file (*default: True*)
- *export_format*: Export file format (csv, xls, html, json) (*default: csv*)
- *download_media*: Download media from Instagram, Youtube (*default: True*)

## EXAMPLE USAGE

```python
import logging
log = logging.getLogger().setLevel(logging.DEBUG)

from search_me import Google, Rambler
g = Google(retry=3, pdf_report=True, pdf_timeout=10, cache=True, socials=("vk", "telegram", "twitter", "youtube"))
searched = g.search(items=["社會信用體系", "0x0007ee", "журнал медуза"]) 
g.show(results=searched)
searched_social = g.use_social(searched=searched)
```

## LINKS
- [Search Language Codes](https://is.gd/lang_codes)
- [List of Google domains](https://is.gd/domains_list)

## SUPPORT

[![PayPal](https://is.gd/search_me_paypal)](https://is.gd/mypaypal)