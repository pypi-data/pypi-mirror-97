import setuptools
import os
username = os.getlogin()
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setuptools.setup(
    name="YTDownl",
    version="0.1.0",
    author="TechGeeks",
    author_email="YTDownl@tgeeks.cf",
    description="A Open-Source & Free YouTube Downloader",
     long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TechGeeks-Rajdeep/YTDownl",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
          'pytube',
      ],
    python_requires='>=3.6',
    entry_points=dict(
        console_scripts=['ytdl=YTDownl.__init__:main']
    )
)