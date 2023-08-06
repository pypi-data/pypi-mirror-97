# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['nsdpy']
install_requires = \
['certifi>=2020.12.5,<2021.0.0',
 'chardet>=4.0.0,<5.0.0',
 'idna>=2.10,<3.0',
 'requests>=2.25.1,<3.0.0',
 'urllib3>=1.26.2,<2.0.0']

entry_points = \
{'console_scripts': ['nsdpy = nsdpy:main']}

setup_kwargs = {
    'name': 'nsdpy',
    'version': '0.1.13',
    'description': 'Automatize the donwload of DNA sequences from NCBI, sort them according to their taxonomy and filter them with a gene name (provided as a regular expression)',
    'long_description': '# nsdpy\n\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n[![pypi](https://img.shields.io/pypi/v/nsdpy)](https://pypi.org/project/nsdpy/)\n\n\n\n- [Introduction](#introduction)\n- [Workfolw](#workflow)\n- [Quick start](#quick-start)\n- [Usage](#usage)\n  - [Google Colab](#google-colab)\n  - [Command line](#command-line)\n- [Authors and acknowledgment](#authors-and-acknowledgment)\n- [Support](#support)\n- [Licence](#license)\n- [More Documentation](#more-documentation)\n\n## Introduction\n\nnsdpy (nucleotide or NCBI sequence downloader) aims to ease the download and sort of big bacth of DNA sequences from the NCBI database. \nIt can also be usefull to filter the sequences based on their annotations.\nUsing nsdpy the user can:\n\n- **Search** NCBI nucleotide database\n- **Download** the fasta files or the cds_fasta files corresponding to the result of the search\n- **Sort** the sequences based on their taxonomy\n- **Select** coding sequences from cds files based on the gene names using one or more regular expressions. \nThis can help the user retrieve some sequences for which the gene name is annotated in another field.\n\n## Quick start\n\n- Github: Clone the repo: git clone https://github.com/RaphaelHebert/nsdpy.git\n- pip:  \n```bash \npip install nsdpy\n```\n*minimum python version for nsdpy: 3.8.2* \n\n- Google Colab: save a copy of [this notebook](https://colab.research.google.com/drive/1UmxzRc_k5sNeQ2RPGe29nWR_1_0FRPkq?usp=sharing) in your drive.\n\n## Workflow\n\n<img src="workflow.png" alt="workflow" width="600"/>\n\n## Usage\n### Google colab\n\n[nsdpy colab notebook](https://colab.research.google.com/drive/1UmxzRc_k5sNeQ2RPGe29nWR_1_0FRPkq?usp=sharing)\n\n### Command line\n\n```bash\n      nsdpy -r USER\'S REQUEST [OPTIONS] \n```\n\n## Authors and acknowledgment\n\n## Support\n\n## License\n\nCode and documentation copyright 2021 the nsdpy Authors. Code released under the MIT License.\n\n## More Documentation\n\nFor examples of usage and more detailed documentation check: \n[Users manual on google doc](https://docs.google.com/document/d/1CJQg2Cv3P0lgWZRYd9xJQfj8qwIY4a-wtXa4VERdH2c/edit?usp=sharing=100)\n\n\n',
    'author': 'RaphaelHebert',
    'author_email': 'raphaelhebert18@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/RaphaelHebert/nsdpy',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
