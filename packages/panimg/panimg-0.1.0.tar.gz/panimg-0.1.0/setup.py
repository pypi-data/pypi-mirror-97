# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['panimg', 'panimg.image_builders']

package_data = \
{'': ['*']}

install_requires = \
['Pillow',
 'SimpleITK',
 'numpy',
 'openslide-python',
 'pydantic',
 'pydicom',
 'pyvips',
 'tifffile==2019.1.4']

setup_kwargs = {
    'name': 'panimg',
    'version': '0.1.0',
    'description': 'Conversion of medical images to MHA and TIFF.',
    'long_description': '# panimg\n\n[![CI](https://github.com/DIAGNijmegen/rse-panimg/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/DIAGNijmegen/rse-panimg/actions/workflows/ci.yml?query=branch%3Amain)\n![PyPI](https://img.shields.io/pypi/v/panimg)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/panimg)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n**NOT FOR CLINICAL USE**\n\nConversion of medical images to MHA and TIFF. \nRequires Python 3.7, 3.8 or 3.9.\n`libvips-dev` and `libopenslide-dev` must be installed on your system.\nFor compressed DICOM support ensure that `gdcm` is installed.\n\nUnder the hood we use:\n\n* `SimpleITK`\n* `pydicom`\n* `Pillow`\n* `openslide-python`\n* `pyvips`\n\n## Usage\n\n`panimg` takes a folder full of files and tries to covert them to MHA or TIFF.\nFor each subdirectory of files it will try several strategies for loading the contained files, and if an image is found it will output it to the output folder.\nIt will return a structure containing information about what images were produced, what images were used to form the new images, image metadata, and any errors from any of the strategies.\n\n**NOTE: Alpha software, do not run this on folders you do not have a backup of.**\n\n```python\nfrom pathlib import Path\nfrom panimg import convert\n\nresult = convert(\n    input_directory=Path("/path/to/files/"),\n    output_directory=Path("/where/files/will/go/"),\n)\n```\n\n### Supported Formats\n\n| Input                               | Output           | Strategy   | Notes                      |\n| ----------------------------------- | ---------------- | ---------- | -------------------------- |\n| `.mha`                              | `.mha`           | `metaio`   |                            |\n| `.mhd` with `.raw` or `.zraw`       | `.mha`           | `metaio`   |                            |\n| `.dcm`                              | `.mha`           | `dicom`    | <sup>[1](#footnote1)</sup> |\n| `.nii`                              | `.mha`           | `nifty`    |                            |\n| `.nii.gz`                           | `.mha`           | `nifty`    |                            |\n| `.png`                              | `.mha`           | `fallback` | <sup>[2](#footnote2)</sup> |\n| `.jpeg`                             | `.mha`           | `fallback` | <sup>[2](#footnote2)</sup> |\n| `.tiff`                             | `.tiff` & `.dzi` | `tiff`     | <sup>[3](#footnote3)</sup> |\n| `.svs` (Aperio)                     | `.tiff` & `.dzi` | `tiff`     | <sup>[3](#footnote3)</sup> |\n| `.vms`, `.vmu`, `.ndpi` (Hamamatsu) | `.tiff` & `.dzi` | `tiff`     | <sup>[3](#footnote3)</sup> |\n| `.scn` (Leica)                      | `.tiff` & `.dzi` | `tiff`     | <sup>[3](#footnote3)</sup> |\n| `.mrxs` (MIRAX)                     | `.tiff` & `.dzi` | `tiff`     | <sup>[3](#footnote3)</sup> |\n| `.biff` (Ventana)                   | `.tiff` & `.dzi` | `tiff`     | <sup>[3](#footnote3)</sup> |\n\n<a name="footnote1">1</a>: Compressed DICOM requires `gdcm`\n\n<a name="footnote2">2</a>: 2D only, unitary dimensions\n\n<a name="footnote3">3</a>: DZI only created if possible\n',
    'author': 'James Meakin',
    'author_email': '12661555+jmsmkn@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/DIAGNijmegen/rse-panimg',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
