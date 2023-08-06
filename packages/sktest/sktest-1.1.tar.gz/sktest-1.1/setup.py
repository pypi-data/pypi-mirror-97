# -*- coding:utf8 -*-
# @author：X.
# @time：2020/9/18:10:33


from setuptools import setup, find_packages

# with open("README.md", "r", encoding="utf-8") as fh:
#     long_description = fh.read()

setup(
    name="sktest",  # 包名字
    version="1.1",
    url="https://github.com/cxyboy/sktest",  #
    description="A library of tools to quickly expand UI testing",
    # long_description=long_description,  # 将说明文件设置为README.md
    long_description_content_type="text/markdown",
    packages=find_packages(),  # 默认从当前目录下搜索包
    author="xuluocan",
    author_email="hijackx@163.com",
    classifiers=[  # 只适用于python3
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['selenium==3.141.0', 'openpyxl==3.0.5', 'Pillow==7.2.0', 'xlrd==1.2.0', 'xlsxwriter==1.3.3',
                      'pypiwin32==223'],
    python_requires='>=3.5',
)
