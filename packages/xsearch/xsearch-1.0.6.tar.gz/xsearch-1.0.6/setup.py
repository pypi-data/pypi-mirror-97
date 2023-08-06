import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="xsearch",
    version="1.0.6",
    author="Yuqing Xue",
    author_email="xueyuqing98@163.com",
    description="Search, export and analyse more efficiently",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/YuqingXue/xsearch",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
)
