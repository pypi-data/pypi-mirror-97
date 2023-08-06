# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tagfiles']

package_data = \
{'': ['*']}

install_requires = \
['mutagen>=1.42,<2.0']

setup_kwargs = {
    'name': 'tagfiles',
    'version': '0.3.3',
    'description': 'A tagging interface for multiple audio formats and metadata containers.',
    'long_description': '# tagfiles\n\n[![CI](https://img.shields.io/github/workflow/status/azuline/tagfiles/CI)](https://github.com/azuline/tagfiles/actions)\n[![codecov](https://img.shields.io/codecov/c/github/azuline/tagfiles?token=VF37TOZ5HJ)](https://codecov.io/gh/azuline/tagfiles)\n[![Pypi](https://img.shields.io/pypi/v/tagfiles.svg)](https://pypi.python.org/pypi/tagfiles)\n[![Pyversions](https://img.shields.io/pypi/pyversions/tagfiles.svg)](https://pypi.python.org/pypi/tagfiles)\n\nA tagging interface for multiple audio formats and metadata containers.\n\nThe supported audio codecs and containers are:\n\n- FLAC in FLAC container\n- MP3 in MP3 container\n- AAC in MP4 container\n- Vorbis in Ogg container\n- Opus in Ogg container\n\nTag mappings are derived from https://picard.musicbrainz.org/docs/mappings/ .\n\n## Usage\n\n```python\n>>> from tagfiles import TagFile, ArtistRoles\n>>> from pprint import pprint\n>>>\n>>> tf = TagFile(\'/home/azuline/02. No Captain.m4a\')\n>>> print(tf.title)\nNo Captain\n>>> pprint(tf.artist)\n{<ArtistRoles.MAIN: 1>: [\'Lane 8\'],\n <ArtistRoles.FEATURE: 2>: [\'Poliça\'],\n <ArtistRoles.REMIXER: 3>: [],\n <ArtistRoles.PRODUCER: 4>: [],\n <ArtistRoles.COMPOSER: 5>: [\'\'],\n <ArtistRoles.CONDUCTOR: 6>: [],\n <ArtistRoles.DJMIXER: 7>: []}\n>>> print(tf.artist[ArtistRoles.MAIN])\n[\'Lane 8\']\n>>> print(tf.date.year)\n2015\n>>> print(tf.date.date)\n2015-01-19\n>>>\n>>> tf.date = \'2018-01-19\'  # Fixing the date!\n>>> print(tf.date.date)\n2018-01-19\n>>> print(tf.date.year)\n2018\n>>> tf.save()\n>>>\n>>> tf = TagFile(\'/home/azuline/music.txt\')\nTraceback (most recent call last):\n  File "<stdin>", line 1, in <module>\n  File "/home/azuline/devel/tagfiles/tagfiles/__init__.py", line 27, in TagFile\n    raise UnsupportedFileType\ntagfiles.errors.UnsupportedFileType\n```\n\nThe TagFile function takes a filepath as a parameter and returns the class\nwhich corresponds to its container. If an unsupported filetype is passed in,\nthe `UnsupportedFileType` error is raised. Each class presents the same metadata\ninterface, which have the following attributes:\n\n```python\ntitle: str\nversion: str\nalbum: str\nartist_album: List[str]\ncatalog_number: str\nrelease_type: str\ncomment: str\ndate.year: int\ndate.date: str\ntrack_number: str\ntrack_total: str\ndisc_number: str\ndisc_total: str\ngenre: List[str]\nlabel: str\nartist = {\n  ArtistRoles.MAIN: List[str]\n  ArtistRoles.FEATURE: List[str]\n  ArtistRoles.REMIXER: List[str]\n  ArtistRoles.PRODUCER: List[str]\n  ArtistRoles.COMPOSER: List[str]\n  ArtistRoles.CONDUCTOR: List[str]\n  ArtistRoles.DJMIXER: List[str]\n}\nimage_mime: str\nimage: bytes\n```\n\nFields can be edited by setting new values to the attributes of the TagFile.\nTo edit the date, which is special, assign a string in the format of `%Y-%m-%d`\nor `%Y` to the `date` attribute. To save the changes made to the tags, call the\n`save()` method.\n\n_Note: Image field is not currently editable._\n',
    'author': 'azuline',
    'author_email': 'azuline@riseup.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/azuline/tagfiles',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
