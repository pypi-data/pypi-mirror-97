from setuptools import setup
 
 
setup(name="androidyt",
version="0.1",
description="Plays Youtube videos on Android like the pywhatkit",
long_description='with Support of Python 3.7',
long_description_content_type='text/markdown',
author="Devesh Baghel",
author_email='unknowtech000@gmail.com',
packages=['packages'],
install_requires=['google-search'],
license="MIT",
classifiers=[
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 3.6",
                                "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8"
],
install_package_data=True,
 
)