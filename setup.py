#!/usr/bin/env python3 

from setuptools import setup

setup(
	name = "Unique-Image-Sort",
	version = "1.0",
	description = "Sort through directories and find unique images",
	install_requires = ['pillow'],
	author = "Hannah Ward",
	author_email = "hannah.ward9001@gmail.com",
	scripts = ["unique-image-sort.py"]
)
