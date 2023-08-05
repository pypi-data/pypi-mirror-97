import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="xsearch",
    version="0.0.2",
    author="Yuqing Xue",
    author_email="xueyuqing98@163.com",
    description="Search, export and analyse more efficiently",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

# 'bing.com' 'cn.bing.com'
# 'google.com' 'google.com.hk'
