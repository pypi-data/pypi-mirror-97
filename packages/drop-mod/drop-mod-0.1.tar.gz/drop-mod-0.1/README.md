# Drop
###### *also known as drop-moderation*
Drop is a Python module focused on providing moderation commands for chat-bots (i.e. Discord, Matrix.org, etc.)
## How do I install/use it?
Unfortunately I have not yet made this package a terminal app, so you'll have to use it in scripts (for example, [drop-discord](https://github.com/AtlasC0R3/drop-discord/))
1. Clone this repository, [by downloading this repository as a \*.zip file](https://github.com/AtlasC0R3/drop-moderation/archive/main.zip), [by cloning this repository using Git](https://github.com/AtlasC0R3/drop-moderation.git) or [by going into this repository's releases](https://github.com/AtlasC0R3/drop-moderation/releases) and downloading the latest release. 
2. Run `setup.py` using your preferred Python installation

Drop should be installed *unless `setup.py` threw an error*!

To use it, import `drop` into your Python scripts (or specific commands using `from drop.basic import owofy`) and, well, use them!

Example:
```python
from drop.basic import owofy
owofy("The quick brown fox jumps over the lazy dog.")
# This is just a simple command to work with, hence why I use it as a prime example.
# no im not a furry shhHHHHHH.
```

### Dependencies
**None of these packages listed below are included directly into this software!** They are only installed from [PyPI](https://pypi.org/) when running `setup.py`!

[duckduckpy](https://github.com/ivankliuk/duckduckpy/), licensed under [MIT License](https://github.com/ivankliuk/duckduckpy/blob/master/LICENSE)

[LyricsGenius](https://github.com/johnwmillr/LyricsGenius/), licensed under [MIT License](https://github.com/johnwmillr/LyricsGenius/blob/master/LICENSE.txt)

[Parsedatetime](https://github.com/bear/parsedatetime/), licensed under [Apache 2.0](https://github.com/bear/parsedatetime/blob/master/LICENSE.txt)
