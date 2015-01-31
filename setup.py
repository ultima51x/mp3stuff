from distutils.core import setup

setup(
    name="mp3stuff",
    version="0.0.1",
    author="David Hwang",
    author_email="d.hw4ng@gmail.com",
    packages=["mp3stuff"],
    scripts=["bin/id3validate","bin/diffmusic","bin/albumart","bin/albumartcrawl"],
    description="This does id3 stuff",
    install_requires=[
        "eyeD3 >= 0.7.4",
        "termcolor >= 1.1.0",
        "Pillow >= 2.0.0",
        "mutagen >= 1.27"
    ],
)
