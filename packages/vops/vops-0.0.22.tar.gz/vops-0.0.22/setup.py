from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="vops",
    version="0.0.22",
    author="Ryan Lee",
    author_email="ryanjlee22@gmail.com",
    description="A package for graphing profit-loss option diagrams",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RJL22/vops",
    package_dir={"": 'src'},
    packages=find_packages(
    	where="src"
    	),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires= [
    "beautifulsoup4==4.9.3",
	"bs4==0.0.1",
	"certifi==2020.11.8",
	"chardet==3.0.4",
	"cycler==0.10.0",
	"idna==2.10",
	"kiwisolver==1.3.1",
	"lxml==4.6.1",
	"matplotlib==3.3.3",
	"numpy==1.19.4",
	"pandas==1.1.4",
	"Pillow==8.0.1",
	"pyparsing==2.4.7",
	"python-dateutil==2.8.1",
	"pytz==2020.4",
	"requests==2.25.0",
	"six==1.15.0",
	"soupsieve==2.0.1",
	"urllib3==1.26.2",
    ],
    python_requires='>=3.6',
)