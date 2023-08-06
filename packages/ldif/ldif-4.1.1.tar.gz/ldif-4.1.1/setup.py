# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

modules = \
['ldif']
setup_kwargs = {
    'name': 'ldif',
    'version': '4.1.1',
    'description': 'generate and parse LDIF data (see RFC 2849).',
    'long_description': '# ldif - parse and generate LDIF data (see [RFC 2849](https://tools.ietf.org/html/rfc2849)).\n\n![Commit activity](https://img.shields.io/github/commit-activity/m/abilian/ldif)\n![Code size in bytes](https://img.shields.io/github/languages/code-size/abilian/ldif)\n![License](https://img.shields.io/github/license/abilian/ldif)\n![Latest version](https://img.shields.io/pypi/v/ldif)\n![PyPI Downloads](https://img.shields.io/pypi/dm/ldif)\n\nThis is a fork of the `ldif` module from\n[python-ldap](http://www.python-ldap.org/) with python3/unicode support.\n\nOne of its benefits is that it\'s a pure-python package (you don\'t\ndepend on the `libldap2-dev` (or similar) package that needs to be\ninstalled on your laptop / test machine / production server).\n\nSee the first entry in changelog below for a more complete list of\ndifferences.\n\nThis package only support Python 3 (\\>= 3.7, actually).\n\n\n## Usage\n\nParse LDIF from a file (or `BytesIO`):\n\n```python\nfrom ldif import LDIFParser\nfrom pprint import pprint\n\nparser = LDIFParser(open("data.ldif", "rb"))\nfor dn, record in parser.parse():\n    print(\'got entry record: %s\' % dn)\n    pprint(record)\n```\n\nWrite LDIF to a file (or `BytesIO`):\n\n```python\nfrom ldif import LDIFWriter\n\nwriter = LDIFWriter(open("data.ldif", "wb"))\nwriter.unparse("mail=alice@example.com", {\n    "cn": ["Alice Alison"],\n    "mail": ["alice@example.com"],\n    "objectclass": ["top", "person"],\n})\n```\n\n\n## Unicode support\n\nThe stream object that is passed to parser or writer must be an ascii\nbyte stream.\n\nThe spec allows to include arbitrary data in base64 encoding or via URL.\nThere is no way of knowing the encoding of this data. To handle this,\nthere are two modes:\n\nBy default, the `LDIFParser` will try to interpret all values as UTF-8\nand leave only the ones that fail to decode as bytes. But you can also\npass an `encoding` of `None` to the constructor, in which case the\nparser will not try to do any conversion and return bytes directly.\n',
    'author': 'Abilian SAS',
    'author_email': 'dev@abilian.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/abilian/ldif',
    'package_dir': package_dir,
    'py_modules': modules,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
