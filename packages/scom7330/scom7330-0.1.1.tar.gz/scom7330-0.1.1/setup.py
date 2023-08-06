# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['scom7330', 'scom7330.config']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['scom_audiolib_tool = scom7330.audiolib_tool:main']}

setup_kwargs = {
    'name': 'scom7330',
    'version': '0.1.1',
    'description': 'A tool to manipulate various data, including Audio Libraries (ex CustomAudioLib.bin) for the SCOM 7330 repeater',
    'long_description': "# SCOM 7330 Speech Library Tool\n\n![Unit Tests](https://github.com/ad1217/SCOM7330_SpeechLib_Tool/workflows/Unit%20Tests/badge.svg)\n\nThis is a tool to manipulate Audio Libraries (such as\n`CustomAudioLib.bin`) for the SCOM 7330 repeater, reverse engineered\nfrom the provided `BuildSpeechLib.exe`.\n\nThe official tool, as well as default audio libraries, manuals,\nfirmware, etc. can be found at\nhttp://www.scomcontrollers.com/7330firmware .\n\n## Speech Library Format\n\n**Remember that this is reverse engineered (so not guaranteed to be\naccurate), and subject to change with firmware updates**\n\n**This was derived from firmware release V1.8b,\n  BuildSpeechLib.exe V1.2.0 (built 5/13/2018)**\n\nThe speech library file is composed of 4 sections:\n\n- [Header](#header) (`0x100` bytes)\n- [Image Header](#image-header) (`0x100` bytes)\n- [Word Index](#word-index) (variable length, rounded up to the nearest `0x100`)\n- [Word Data](#word-data) (variable length)\n\nThe header and image header contain metadata and the word index is a\nlookup table into the data. Unused space is filled with `0xff` instead\nof `0x00`, for unclear reasons.\n\nIn the following sections, byte ranges are presented as\n`inclusive:exclusive`, like in Python. For example, `0x00:0x05`\nincludes the bytes `0x00`, `0x01`, `0x02`, `0x03`, and `0x04`. All\naddresses in tables are relative to the start of the section, unless\nstated otherwise.\n\n### Header\n\n- Address: `0x00`\n- Length: `0x100`\n\n| Byte  | 0x00:0x05  | 0x05:0x15 | 0x15:0x21 | 0x21:0x38 | 0x38 | 0x39:0x3c | 0x3c:0x3d | 0x3d:0x100 |\n|:------|:-----------|:----------|:----------|:----------|:-----|:----------|:----------|:-----------|\n| Value | `SCOM\\x00` | name      | version   | timestamp | mode | firstFree | zeros     | (empty)    |\n\n- `name`, `version`, and `timestamp` are just ASCII strings, and have\n  no apparent function beyond display.\n- `mode` is 3 in `BuildSpeechLib.exe`'s normal mode, 2 in the extended\n  arguments form. I am not sure what this means, exactly.\n- `firstFree` is the size of the file minus `0x100`, presumably to\n  account for this header's size. Unclear what this is used for, as it\n  also occurs (with the `0x100` included) in the [Image Header](#image-header)\n- `zeros` is two two-byte arguments to the function in\n  `BuildSpeechLib.exe` which were passed in as literal zeros. Unclear\n  function.\n\n### Image Header\n\n- Address: `0x100`\n- Length: `0x100`\n\n| Byte  | 0x00:0x03      | 0x03           | 0x04:0x06    | 0x06:0x09 | 0x09:0x100 |\n|:------|:---------------|:---------------|:-------------|:----------|:-----------|\n| Value | `\\x00\\x02\\x00` | index_size_mid | max_word + 1 | firstFree | (empty)    |\n\n- I'm not sure what the purpose of the constant in `0x00:0x03` is\n- `index_size_mid` is the middle byte of the [Word Index](#word-index)\n  size. Since that size is rounded to `0x100`, this is just the index\n  size shifted down 1 byte.\n- `max_word + 1` is the highest word file contained, plus one.\n  Not really sure why it's plus one.\n- `firstFree` is the length of the file.\n  Seems to be redundant with the value in the [Header](#header).\n\n### Word Index\n\n- Address: `0x200`\n- Length: 4 times the maximum word code, rounded up to the nearest `0x100`\n\n| Byte  | (word code * 4):(word code * 4) + 3 |\n|:------|:------------------------------------|\n| Value | word data address                   |\n\nThis section is a lookup table mapping the word code to the address of\nthe entry in the [Word Data](#word-data) section, relative to the file\nstart. All un-used entries are blank (`0xff`). Each entry is 4 bytes\nlong, but the address is stored just in the first 3 bytes (with the\nlast one being `0xff`.\n\n### Word Data\n\n- Address: `0x200` plus the the length of the [Word Index](#word-index),\n  as stored in the [Image Header](#image-header).\n- Length: 3 times the number of files, plus the length of each file\n\nFor each entry:\n| Byte  | 0x00:0x03                | 0x03:end of file |\n|:------|:-------------------------|:-----------------|\n| Value | end of file data address | file data        |\n\n- `end of file data address` is the address of the end of the audio file data.\n- `file data` is the contents of a raw file (as per\n  [Audio Files](#audio-files)), but with every byte greater than 127 xor'ed\n  with 127 for some unclear reason.\n\n\n## Audio Files\n\nThe input/output audio files are in the format specified in the SCOM manual:\n\n- 8000 Hertz sampling rate\n- Single channel (mono) audio\n- μ-law encoding\n- Raw headerless file\n\nYou can convert wav files (for example) to this format with `sox`:\n\n```sh\nsox --type wav <input file>.wav --type ul --rate 8k <output file>.raw\n```\n\nor from this format to wav:\n\n```sh\nsox --type ul --rate 8k --channels 1 <input file>.raw --type wav <output file>.wav\n```\n\n\n## Disclaimer\n\nI am not affiliated with S-COM in any way. I make no guarantees of the\ncorrectness of the code. Don't break your stuff.\n",
    'author': 'Adam Goldsmith',
    'author_email': 'adam@adamgoldsmith.name',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ad1217/python-SCOM7330',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
