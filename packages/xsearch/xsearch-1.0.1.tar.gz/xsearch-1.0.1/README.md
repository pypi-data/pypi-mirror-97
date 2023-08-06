English | [简体中文](./README.CN.md)

# xsearch

## About The Project

Use Python to search, export and analyse the search results of a long list of keywords.

### Built With

[Selenium](https://selenium-python.readthedocs.io/) A package to automate web browser interaction from Python.

## Getting Started

### Prerequisites

***Python***    Python 3

***Chrome***    Download Google Chrome, and check the version through 'Help > About Google Chrome'.



***ChromeDriver***  Download a driver to interface with the Chrome browser. Make sure it’s consistent with Chrome version.
[link1](https://sites.google.com/a/chromium.org/chromedriver/downloads) [link2](http://npm.taobao.org/mirrors/chromedriver/) [link3](https://chromedriver.storage.googleapis.com/index.html)


### Installation

If you have [pip](https://pip.pypa.io/en/stable/) on your system, you can simply install or upgrade the Python bindings:

`pip install search`

Alternately, you can download the source code from [PyPI](https://pypi.org/project/xsearch/#files) (e.g. xsearch-0.0.8.tar.gz), unarchive it, and run:

`python setup.py install`

## Usage

### Search Engines 

- google.com *or* google.com.hk

- baidu.com

- bing.com *or* cn.bing.com

- sogou.com
  
- weixin.sogou.com

### Code

```
import xsearch
xsearch.search()
```

## License

The project is under the [MIT](./LICENSE.txt) license.


