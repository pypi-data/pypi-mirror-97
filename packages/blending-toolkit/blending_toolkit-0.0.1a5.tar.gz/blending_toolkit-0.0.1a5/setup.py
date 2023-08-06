# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['btk']

package_data = \
{'': ['*']}

install_requires = \
['astropy>=4.2,<5.0',
 'galsim>=2.2.4,<3.0.0',
 'matplotlib>=3.3.3,<4.0.0',
 'numpy>=1.18.5,<2.0.0',
 'scikit-image>=0.18.0,<0.19.0',
 'scipy>=1.4.1,<2.0.0',
 'sep>=1.1.1,<2.0.0']

setup_kwargs = {
    'name': 'blending-toolkit',
    'version': '0.0.1a5',
    'description': 'Blending ToolKit',
    'long_description': '![tests](https://github.com/LSSTDESC/BlendingToolKit/workflows/tests/badge.svg)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![codecov](https://codecov.io/gh/LSSTDESC/BlendingToolKit/branch/main/graph/badge.svg)](https://codecov.io/gh/LSSTDESC/BlendingToolKit)\n\n**NOTE:** BTK is currently undergoing heavy development and rapidly changing, as such the documentation and most jupyter could be deprecated. Please feel free to contact [@ismael-mendoza](https://github.com/ismael-mendoza) if you would like to use `BTK` for a current project or contribute.\n# BlendingToolKit\nFramework for fast generation and analysis of galaxy blends catalogs. This toolkit is a convenient way of\nproducing multi-band postage stamp images of blend scenes.\n\nDocumentation can be found at https://lsstdesc.org/BlendingToolKit/index.html\n\n## Workflow\n<img src="docs/source/images/current_flowchart.png" alt="btk workflow" width="450"/>\n\nColor code for this flowchart :\n- Classes in black should be used as is by the user.\n- Classes in red may be reimplemented by the experienced user ; we recommend for new users to use the default implementations until they are familiar with them.\n- In blue is the code for instantiating the classes within the code (optional arguments not included).\n- In green are the revelant methods for the classes ; please note that the `__call__` method is executed when calling the object (eg `sampling_function(catalog)`) and the `__next__` method is executed when using `next` (eg `next(generator)`).\n\n## Running BlendingToolKit\n- BlendingToolKit (btk) requires an input catalog that contains information required to simulate galaxies and blends.\nThis repository includes sample input catalogs with a small number of galaxies that can be used to draw blend images with btk. See [tutorials](https://github.com/LSSTDESC/BlendingToolKit/tree/main/notebooks) to learn how to run btk with these catalogs.\n- CatSim Catalog corresponding to one square degree of sky and processed WeakLensingDeblending catalogs can be downloaded from [here](https://stanford.app.box.com/s/s1nzjlinejpqandudjyykjejyxtgylbk).\n- [Cosmo DC2](https://arxiv.org/abs/1907.06530) catalog requires pre-processing in order to be used as input catalog to btk. Refer to this [notebook](https://github.com/LSSTDESC/WeakLensingDeblending/blob/cosmoDC2_ingestion/notebooks/wld_ingestion_cosmoDC2.ipynb) on how to convert the DC2 catalog into a CatSim-like catalog that can be analyzed with btk.\n\n## Installation\nBTK is pip installable, with the following command: \n\n```\npip install blending_toolkit\n```\n\nAlthough you might run into problems installing `galsim`. In case of any issues, please see the more detailed installation instructions [here](https://lsstdesc.org/BlendingToolKit/install.html).\n\nFor required packages, see [pyproject.toml](https://github.com/LSSTDESC/BlendingToolKit/blob/main/pyproject.toml) under the `[tool.poetry.dependencies]` block. For developers, you will also need the packages under the `[tool.poetry.dev-dependencies]` block.\n\n\n## Contributing\n\nSee [CONTRIBUTING.md](https://github.com/LSSTDESC/BlendingToolKit/blob/main/CONTRIBUTING.md)\n',
    'author': 'Ismael Mendoza',
    'author_email': 'imendoza@umich.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/LSSTDESC/BlendingToolKit',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
