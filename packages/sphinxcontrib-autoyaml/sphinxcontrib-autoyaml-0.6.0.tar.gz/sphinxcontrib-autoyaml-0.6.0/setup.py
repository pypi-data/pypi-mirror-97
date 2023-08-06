# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sphinxcontrib', 'sphinxcontrib.autoyaml']

package_data = \
{'': ['*']}

install_requires = \
['Sphinx>=3.5.1,<4.0.0', 'ruamel.yaml>=0.16.12,<0.17.0']

setup_kwargs = {
    'name': 'sphinxcontrib-autoyaml',
    'version': '0.6.0',
    'description': 'Sphinx autodoc extension for documenting YAML files from comments',
    'long_description': '# sphinxcontrib-autoyaml\n\nThis Sphinx autodoc extension documents YAML files from comments. Documentation\nis returned as reST definitions, e.g.:\n\nThis document:\n\n```\n###\n# Enable Nginx web server.\nenable_nginx: true\n\n###\n# Enable Varnish caching proxy.\nenable_varnish: true\n```\n\nwould be turned into text:\n\n```\nenable_nginx\n\n   Enable Nginx web server.\n\nenable_varnish\n\n   Enable Varnish caching proxy.\n```\n\nSee `tests/examples/output/index.yml` and `tests/examples/output/index.txt` for\nmore examples.\n\n`autoyaml` will take into account only comments which first line starts with\n`autoyaml_doc_delimiter`.\n\n## Usage\n\nYou can use `autoyaml` directive, where you want to extract comments\nfrom YAML file, e.g.:\n\n```\nSome title\n==========\n\nDocumenting single YAML file.\n\n.. autoyaml:: some_yml_file.yml\n```\n\n## Options\n\nOptions available to use in your configuration:\n\n- *autoyaml_root*(`..`)\n  Look for YAML files relatively to this directory.\n- *autoyaml_doc_delimiter*(`###`)\n  Character(s) which start a documentation comment.\n- *autoyaml_comment*(`#`)\n  Comment start character(s).\n\n## Installing\n\nIssue command:\n\n```\npip install sphinxcontrib-autoyaml\n```\n\nAnd add extension in your project\'s ``conf.py``:\n\n```\nextensions = ["sphinxcontrib.autoyaml"]\n```\n',
    'author': 'Jakub Pieńkowski',
    'author_email': 'jakub+sphinxcontrib-autoyaml@jakski.name',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Jakski/sphinxcontrib-autoyaml',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
