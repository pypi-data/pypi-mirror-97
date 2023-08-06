from setuptools import setup
 
 
setup(name="androidyt",
version="1.1",
description="Plays Youtube videos on Android like the pywhatkit",
long_description='Use playonyt() function',
author="Devesh Baghel",
author_email='unknowtech000@gmail.com',
packages=['packages'],
install_requires=['google-search'],
license="MIT",
classifiers=[
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.8"
],
install_package_data=True,
 
)