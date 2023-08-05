# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['imctools',
 'imctools.converters',
 'imctools.data',
 'imctools.io',
 'imctools.io.imc',
 'imctools.io.mcd',
 'imctools.io.ometiff',
 'imctools.io.txt']

package_data = \
{'': ['*']}

install_requires = \
['imagecodecs>=2020.5.30,<2021.0.0',
 'packaging',
 'pandas>=1.0,<2.0',
 'typing_extensions>=3.7.4.2',
 'xmltodict>=0.12.0',
 'xtiff>=0.6.4']

entry_points = \
{'console_scripts': ['imctools = imctools.cli:main']}

setup_kwargs = {
    'name': 'imctools',
    'version': '2.1.5',
    'description': 'Tools to handle Fluidigm IMC data',
    'long_description': '# imctools\n\n[![Build Status](https://github.com/BodenmillerGroup/imctools/workflows/CI/badge.svg)](https://github.com/BodenmillerGroup/imctools/workflows/CI/badge.svg)\n[![PyPI version](https://badge.fury.io/py/imctools.svg)](https://pypi.python.org/pypi/imctools)\n\n> `imctools` v2.x has many changes in IMC data output format, available CLI commands, dropped Python 2 and Fiji plugins support, etc.\n> If you are using `imctools` in pre-processing pipelines, please install v1.x version until your pipeline is modified accordingly!\n> We strongly encourage you to migrate to `imctools` v2.x as all further efforts will be focused on a development of this version.\n\nAn IMC file conversion tool that aims to convert IMC raw data files (.mcd, .txt) into an intermediary ome.tiff, containing all the relevant metadata. Further it contains tools to generate simpler TIFF files that can be directly be used as input files for e.g. CellProfiller, Ilastik, Fiji etc.\n\nFor a description of the associated segmentation pipline, please visit: https://github.com/BodenmillerGroup/ImcSegmentationPipeline\n\nVersion 2.x documentation: https://bodenmillergroup.github.io/imctools\n\nVersion 1.x documentation (deprecated): https://imctools.readthedocs.io\n\n## Features\n\n- MCD lazy data access using memorymaps\n- Full MCD metadata access\n- TXT file loading\n- OME-TIFF loading\n- OME-TIFF/TIFF export (including optional compression)\n\n## Prerequisites\n\n- Supports Python 3.7 or newer\n- External dependencies: `imagecodecs`, `pandas`, `xmltodict`, `xtiff`.\n\n## Installation\n\nPreferable way to install `imctools` is via official PyPI registry. Please define package version explicitly in order to avoid incompatibilities between v1.x and v2.x versions:\n```\npip install imctools==2.1.4\n```\nIn old IMC segmentation pipelines versions 1.x should be used!\n```\npip install imctools==1.0.8\n```\n\n## Usage of version 2.x\n\n`imctools` is often used from Jupyter as part of the pre-processing pipeline, mainly using the __converters__ wrapper functions. Please check the [following example](https://github.com/BodenmillerGroup/ImcSegmentationPipeline/blob/development/scripts/imc_preprocessing.ipynb) as a template.\n\nFurther `imctools` can be directly used as a module:\n\n```python\nfrom imctools.io.mcd.mcdparser import McdParser\n\nfn_mcd = "/home/vitoz/Data/varia/201708_instrument_comp/mcd/20170815_imccomp_zoidberg_conc5_acm1.mcd"\n\nparser = McdParser(fn_mcd)\n\n# Get original metadata in XML format\nxml = parser.get_mcd_xml()\n\n# Get parsed session metadata (i.e. session -> slides -> acquisitions -> channels, panoramas data)\nsession = parser.session\n\n# Get all acquisition IDs\nids = parser.session.acquisition_ids\n\n# The common class to represent a single IMC acquisition is AcquisitionData class.\n# Get acquisition data for acquisition with id 2\nac_data = parser.get_acquisition_data(2)\n\n# imc acquisitions can yield the image data by name (tag), label or index\nchannel_image1 = ac_data.get_image_by_name(\'Ir191\')\nchannel_image2 = ac_data.get_image_by_label(\'Histone_phospho_125((2468))Eu153\')\nchannel_image3 = ac_data.get_image_by_index(7)\n\n# or can be used to save OME-TIFF files\nfn_out =\'/home/vitoz/temp/test.ome.tiff\'\nac_data.save_ome_tiff(fn_out, names=[\'Ir191\', \'Yb172\'])\n\n# save multiple standard TIFF files in a folder\nac_data.save_tiffs("/home/anton/tiffs", compression=0, bigtiff=False)\n\n# as the mcd object is using lazy loading memory maps, it needs to be closed\n# or used with a context manager.\nparser.close()\n```\n\n### Usage of previous version 1.x\n\n```python\nimport imctools.io.mcdparser as mcdparser\nimport imctools.io.txtparser as txtparser\nimport imctools.io.ometiffparser as omeparser\nimport imctools.io.mcdxmlparser as meta\n\nfn_mcd = \'/home/vitoz/Data/varia/201708_instrument_comp/mcd/20170815_imccomp_zoidberg_conc5_acm1.mcd\'\n\nmcd = mcdparser.McdParser(fn_mcd)\n\n# parsed Metadata Access\nmcd.acquisition_ids\nmcd.get_acquisition_channels(\'1\')\nmcd.get_acquisition_description(\'1\')\n\n# a metadata object for comprehensive metadata access\nacmeta = mcd.meta.get_object(meta.ACQUISITION, \'1\')\nacmeta.properties\n\n# The common class to represent a single IMC acquisition is\n# The IMC acuqisition class.\n# All parser classes have a \'get_imc_acquisition\' method\nimc_ac = mcd.get_imc_acquisition(\'1\')\n\n# imc acquisitions can yield the image data\nimage_matrix = imc_ac.get_img_by_metal(\'Ir191\')\n\n# or can be used to save the images using the image writer class\nfn_out =\'/home/vitoz/temp/test.ome.tiff\'\nimg = imc_ac.get_image_writer(filename=fn_out, metals=[\'Ir191\', \'Yb172\'])\nimg.save_image(mode=\'ome\', compression=0, dtype=None, bigtiff=False)\n\n# as the mcd object is using lazy loading memory maps, it needs to be closed\n# or used with a context manager.\nmcd.close()\n```\n',
    'author': 'Vito Zanotelli',
    'author_email': 'vito.zanotelli@uzh.ch',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/BodenmillerGroup/imctools',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
