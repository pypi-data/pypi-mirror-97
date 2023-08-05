# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['splink']

package_data = \
{'': ['*'],
 'splink': ['files/*',
            'files/chart_defs/*',
            'files/external_js/*',
            'files/templates/*']}

install_requires = \
['jsonschema>=3.2,<4.0', 'typeguard>=2.10.0,<3.0.0']

setup_kwargs = {
    'name': 'splink',
    'version': '1.0.4',
    'description': "Implementation in Apache Spark of the EM algorithm to estimate parameters of Fellegi-Sunter's canonical model of record linkage.",
    'long_description': "![image](https://user-images.githubusercontent.com/7570107/85285114-3969ac00-b488-11ea-88ff-5fca1b34af1f.png)\n\n[![Coverage Status](https://coveralls.io/repos/github/moj-analytical-services/splink/badge.svg?branch=master)](https://coveralls.io/github/moj-analytical-services/splink?branch=master)\n![issues-status](https://img.shields.io/github/issues-raw/moj-analytical-services/splink)\n![python-version-dependency](https://img.shields.io/badge/python-%3E%3D3.6-blue)\n\n\n# splink: Probabilistic record linkage and deduplication at scale\n\n`splink` implements Fellegi-Sunter's canonical model of record linkage in Apache Spark, including EM algorithm to estimate parameters of the model.\n\nThe aims of `splink` are to:\n\n- Work at much greater scale than current open source implementations (100 million records +).\n\n- Get results faster than current open source implementations - with runtimes of less than an hour.\n\n- Have a highly transparent methodology, so the match scores can be easily explained both graphically and in words\n\n- Have accuracy similar to some of the best alternatives\n\n## Installation\n\n`splink` is a Python package.  It uses the Spark Python API to execute data linking jobs in a Spark cluster.  It has been tested in Apache Spark 2.3 and 2.4.\n\nInstall splink using\n\n`pip install splink`\n\n## Interactive demo\n\nYou can run demos of `splink` in an interactive Jupyter notebook by clicking the button below:\n\n[![Binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/moj-analytical-services/splink_demos/master?urlpath=lab/tree/index.ipynb)\n\n## Documentation\n\nThe best documentation is currently a series of demonstrations notebooks in the [splink_demos](https://github.com/moj-analytical-services/splink_demos) repo.\n\nWe also provide an interactive `splink` settings editor and example settings [here](https://moj-analytical-services.github.io/splink_settings_editor/).  A tool to generate custom `m` and `u` probabilities can be found [here](https://observablehq.com/@robinl/m-and-u-probabilities).\n\nThe statistical model behind `splink` is the same as that used in the R [fastLink package](https://github.com/kosukeimai/fastLink).  Accompanying the fastLink package is an [academic paper](http://imai.fas.harvard.edu/research/files/linkage.pdf) that describes this model.  This is the best place to start for users wanting to understand the theory about how `splink` works.\n\nYou can read a short blog post about `splink` [here](https://robinlinacre.com/introducing_splink/).\n\n## Videos\n\nYou can find a short video introducing `splink` and running though an introductory demo [here](https://www.youtube.com/watch?v=_8lV2Lbd6Xs&feature=youtu.be&t=1295).\n\nA 'best practices and performance tuning' tutorial can be found [here](https://www.youtube.com/watch?v=HzcqrRvXhCE).\n\n## Acknowledgements\n\nWe are very grateful to [ADR UK](https://www.adruk.org/) (Administrative Data Research UK) for providing funding for this work as part of the [Data First](https://www.adruk.org/our-work/browse-all-projects/data-first-harnessing-the-potential-of-linked-administrative-data-for-the-justice-system-169/) project.\n\nWe are also very grateful to colleagues at the UK's Office for National Statistics for their expert advice and peer review of this work.\n",
    'author': 'Robin Linacre',
    'author_email': 'robinlinacre@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/moj-analytical-services/splink',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
