## About The Project

Use Python to search, export and analyse the search results of a long list of keywords.

### Built With

[Selenium](https://selenium-python.readthedocs.io/) A package to automate web browser interaction from Python.

## Getting Started

### Prerequisites

***Python***        Python 3

***Chrome***        Download Google [Chrome](https://www.google.com/intl/en_ca/chrome/), and check the version through 'Help > About Google Chrome'.



***ChromeDriver***      Download a driver to interface with the Chrome browser. Make sure it’s consistent with Chrome version.
[link1](https://sites.google.com/a/chromium.org/chromedriver/downloads) [link2](http://npm.taobao.org/mirrors/chromedriver/) [link3](https://chromedriver.storage.googleapis.com/index.html)


### Installation

If you have [pip](https://pip.pypa.io/en/stable/) on your system, you can simply install or upgrade the Python bindings:

`pip install search`

Alternately, you can download the source code from [PyPI](https://pypi.org/project/xsearch/#files) (e.g. xsearch-0.0.8.tar.gz), unarchive it, and run:

`python setup.py install`

## Usage

### Search Engines Supported

- google.com *or* google.com.hk

- baidu.com

- bing.com *or* cn.bing.com

- sogou.com
  
- weixin.sogou.com

### Code

```Python
import xsearch
xsearch.search()
```

### Example

> **请输入导入文件名，支持txt/xlsx** input.txt
> 
> **请输入指定站点，如有多个用逗号分隔，如无请直接回车** zhihu.com, 36kr.com
>
> **请输入指定文件类型，如有多个用逗号分隔，如无请直接回车** 
>
> **请输入导出文件名，支持csv/json** output.csv
>
> **请输入需要提取的关键词类型，如有多个用逗号分隔，如无请直接回车** n,a,v
>
> **请输入搜索域名** google.com



## License

The project is under the [MIT](./LICENSE.txt) license.


