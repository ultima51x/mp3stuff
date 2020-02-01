# mp3stuff

A lot of random scripts involving MP3s, FLAC, ALAC.  It's a mismash of stuff.

## Setup

It's best to make a virtual environment.  This used Python 3.7.

```sh
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

within the directory

## Development

It's best to use a virtual environment.
```sh
source env/bin/activate
```

To get out of the virtual environemnt
```sh
deactivate
```

Adding a requirement
```sh
pip freeze > requirements.txt
git add requirements.txt
git commit
```

## Usage

Try adding an alias to scripts that are in ./env/bin.

Example: `./env/bin/id3validate`

## Installing it for my Use

```
pipx install .
```
does an install

NOTE: make sure the *.egg-info stuff is not present in the folder.

One would have to re-install it I assume to update it.
