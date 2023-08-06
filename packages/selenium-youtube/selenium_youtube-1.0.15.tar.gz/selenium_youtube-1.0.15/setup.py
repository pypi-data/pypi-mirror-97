import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="selenium_youtube",
    version="1.0.15",
    author="Kovács Kristóf-Attila & Péntek Zsolt",
    description="selenium_youtube",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kkristof200/selenium_youtube",
    packages=setuptools.find_packages(),
    install_requires=[
        'beautifulsoup4>=4.9.3',
        'kcu>=0.0.65',
        'kstopit>=0.0.10',
        'kyoutubescraper>=0.0.2',
        'noraise>=0.0.9',
        'selenium>=3.141.0',
        'selenium-firefox>=1.0.15',
        'selenium-uploader-account>=0.0.9'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)