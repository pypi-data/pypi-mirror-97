from setuptools import setup

setup(name='drop-mod',
      version='0.2',
      description='A Python moderation toolkit built for chat bots',
      url='https://github.com/AtlasC0R3/drop-moderation',
      author='atlas_core',
      license='Apache 2.0',
      packages=['drop'],
      install_requires=[
          "duckduckpy==0.2",
          "lyricsgenius==3.0.0",
          "parsedatetime==2.6"
      ],
      python_requires=">=3.7",
      zip_safe=True)
