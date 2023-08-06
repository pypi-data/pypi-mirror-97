# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tiny_render']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=2.11.3,<3.0.0']

setup_kwargs = {
    'name': 'tiny-render',
    'version': '0.1.3',
    'description': 'A simple wrapper of Jinja2 to render text based file, eg. SQL code and YAML files',
    'long_description': '# Tiny Render\n\nThis is a very simple wrapper for `Jinja2` by providing few built-in variables.\n\nVariables,\n\n- `{{ _gitsha }}` - will be the shortsha for `git` hash, the value will be `None` if `git` is not\ninstalled or the current directory is not a git repo.\n- `{{ \'HOME\' | getenv }}` - the environment variable `HOME` will be renderred. It will raise exception\nif `HOME` is not set\n- `{{ _date_str }}` - the current date in `yyyymmdd` format\n- `{{ _time_str }}` - the current date/time in `yyyymmddHHMMSS` format\n\n\n## Installation\n\n```bash\npip install tiny-render\n```\n\nSample Code\n\n```python\nfrom tiny_render import Render\n\nwith open(os.path.join("/tmp","test.txt"), \'w\') as f:\n    f.write("gitsha: {{_gitsha}}, hello {{key}}")\n\nparams = {"key": "world"}\n\nr = Render("/tmp")\n\nr.go("test.txt", **params)\n\n# the output is "gitsha: xxxxxxx, hello world"\n```',
    'author': 'Zhong Dai',
    'author_email': 'zhongdai.au@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/zhongdai/tiny-render',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
