# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['space_x', 'space_x.utils']

package_data = \
{'': ['*']}

install_requires = \
['arm-mango>=1.1.0,<2.0.0', 'click>=7.1.2,<8.0.0', 'moonline>=0.8.5,<0.9.0']

entry_points = \
{'console_scripts': ['space-x = space_x.space_x:cli']}

setup_kwargs = {
    'name': 'space-x',
    'version': '0.2.0',
    'description': 'A hyperparameter optimizer for MoonLine.',
    'long_description': '# Space-X\nA hyperparameter optimizer for [Moonline](https://gitlab.genzai.dev/boosting-alpha/moonline).\n\n### Running\nTo run Space-X using `poetry`, use the following command:\n```bash\n$ poetry run python space-x -c <config_file>\n```\n\n### Generating Documentation\n```bash\n$ poetry run pdoc --config show_type_annotations=True --html --force space_x/\n```\n\n### Working on Documentation\n`pdoc` can be switched into hot-reload mode by appending the following:\n```bash\n$ poetry run pdoc --config show_type_annotations=True --html --force space_x/ --http :\n```\n\n## Creating A Configuration File\nIn keeping with the way MoonLine handles options, they are specified via a configuration file in [INI](https://en.wikipedia.org/wiki/INI_file) format. This has the added benefit of being able to quickly switch between various configurations simply by pointing it at a different configuration file.\n\n### Example Configuration\n```ini\n[MoonLine]\npath = moonline-config.ini\n\n[SpaceX]\niterations = 10\n\n[Output]\npath = out/\nbest_tearsheet = tearsheet_best.pdf\n\n[Parameters]\npath = params/\nname = ParamsA\n```\n\n### Sections\n#### MoonLine\nDescribes the MoonLine configuration to run.\n##### `path`\nThe path to the MoonLine file configuration file().\n\n#### Space-X\nSpace-X execution options.\n##### `iterations`\nThe number of iterations to run. This giverns how many parameter combinations can be checked. More iterations means more space for testing combinations. This is multiplied by the number of jobs if parallel execution is enabled.\nWhile the iterations will stay fixed (20 by default), if i.e. 4 worker processes are active, 4 times as many parameters will be explored within the same iteration.\n\n#### Output\nPaths for output artifacts.\n##### `path`\nThe path to a directory. If the directory exists, it will be overwritten. This will output sub-directories with MD5 hashes for names containing the output of a specific MoonLine run.\n##### `best_tearsheet`\nThe path to a file (`PDF`). If the file exists, it will be overwritten. This will output a tearsheet in PDF format containing multiple analytical charts to assess the performance of a given strategy. This tearsheet will only be generated for the run with the best parameters.\n\n#### Parameters\nDescribes the parameter space to run.\n##### `path`\nThe path to the directory containing the parameter file(s).\n##### `name`\nEither the exact filename of a parameter file inside the parameter directory (i.e. `crypto_parameters.py`) or the class name of a parameter definition.\n\nIf given a class name, Space-X will automatically look for and instantiate the given parameter class, so you can freely refactor your parameters and rename their files and it will still be able to pick it up.\n\nIf given a filename, only a single parameter class can be contained in the given file. When a class name is given, multiple parameters can be housed in the same file.\n\n## Usage\n```bash\nUsage: space-x [OPTIONS] [ARGS]...\n\nOptions:\n  -c, --config FILE  A file containing Space-X configuration options\n                     [required]\n\n  -v, --verbose\n  --help             Show this message and exit.\n```\n',
    'author': 'Tim Wedde',
    'author_email': 'timwedde@icloud.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.genzai.dev/boosting-alpha/space-x',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
