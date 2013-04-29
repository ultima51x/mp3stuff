from distutils.core import setup

setup(
    name="Id3Stuff",
    version="0.0.1",
    author="David Hwang",
    author_email="d.hw4ng@gmail.com",
    packages=["id3stuff"],
    scripts=["bin/id3validate"],
    description="This does id3 stuff",
    install_requires=[
        "eyeD3 >= 0.7.1",
        "termcolor >= 1.1.0",
    ],
)
