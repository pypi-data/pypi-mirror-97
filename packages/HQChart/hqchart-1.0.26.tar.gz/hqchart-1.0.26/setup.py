from setuptools import setup, find_packages, Distribution
import json

with open('hqchart/pkg_info.json') as fp:
    info = json.load(fp)

setup(
    name = "hqchart",
    version = info["version"],
    author = "jones2000",
    author_email = "jones_2000@163.com",
    description = "HQChartPy2 C++",
    license = "Apache License 2.0",
    keywords = "HQChart HQChartPy2",
    url = "https://github.com/jones2000/HQChart",

    install_requires=['requests', 'pandas', 'numpy'],

    packages=find_packages(include=["hqchart",'hqchart.*py',"hqchart.tushare"]), 

    package_data  = { "hqchart":["*.dll", "HQChartPy2.pyd", "HQChartPy2.so", "pkg_info.json"] },
   
    classifiers=
    [
        'Operating System :: Microsoft :: Windows'
    ],
)