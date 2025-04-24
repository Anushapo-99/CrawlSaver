

### File: setup.py
from setuptools import setup, find_packages

setup(
    name="CrawlSaver",
    version="0.1",
    description="A Python library for managing web scraping interruptions",
    author="Anusha P O, Shahana Farvin",
    packages=find_packages(),
    install_requires=[
        "requests",
        "playwright",
        "selenium",
        "scrapy"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

