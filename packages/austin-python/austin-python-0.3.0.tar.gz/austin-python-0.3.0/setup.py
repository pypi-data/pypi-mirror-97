# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['austin', 'austin.format', 'austin.format.pprof', 'austin.tools']

package_data = \
{'': ['*']}

install_requires = \
['dataclasses',
 'protobuf>=3.12.2,<4.0.0',
 'psutil>=5.7.0',
 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['austin-compress = austin.format.compress:main',
                     'austin2pprof = austin.format.pprof.__main__:main',
                     'austin2speedscope = austin.format.speedscope:main']}

setup_kwargs = {
    'name': 'austin-python',
    'version': '0.3.0',
    'description': 'Python wrapper for Austin, the frame stack sampler for CPython',
    'long_description': '<p align="center">\n  <br/>\n  <img src="docs/source/images/logo.png"\n       alt="Austin"\n       height="256px" />\n  <br/>\n</p>\n\n<h3 align="center">Python wrapper for Austin</h3>\n\n<p align="center">\n  <a href="https://github.com/P403n1x87/austin-python/actions?workflow=Tests">\n    <img src="https://github.com/P403n1x87/austin-python/workflows/Tests/badge.svg"\n         alt="GitHub Actions: Tests">\n  </a>\n  <a href="https://travis-ci.org/P403n1x87/austin-python">\n    <img src="https://travis-ci.org/P403n1x87/austin-python.svg?branch=main"\n         alt="Travis CI">\n  </a>\n  <a href="https://codecov.io/gh/P403n1x87/austin-python">\n    <img src="https://codecov.io/gh/P403n1x87/austin-python/branch/main/graph/badge.svg"\n         alt="Codecov">\n  </a>\n  <a href="https://austin-python.readthedocs.io/">\n    <img src="https://readthedocs.org/projects/austin-python/badge/"\n         alt="Documentation">\n  </a>\n  <br/>\n  <a href="https://pypi.org/project/austin-python/">\n    <img src="https://img.shields.io/pypi/v/austin-python.svg"\n         alt="PyPI">\n  </a>\n  <a href="https://pepy.tech/project/austin-python">\n    <img src="https://static.pepy.tech/personalized-badge/austin-python?period=total&units=international_system&left_color=grey&right_color=blue&left_text=downloads"\n         alt="Downloads" />\n  <a/>\n  <br/>\n  <a href="https://github.com/P403n1x87/austin-python/blob/main/LICENSE.md">\n    <img src="https://img.shields.io/badge/license-GPLv3-ff69b4.svg"\n         alt="LICENSE">\n  </a>\n</p>\n\n<p align="center">\n  <a href="#synopsis"><b>Synopsis</b></a>&nbsp;&bull;\n  <a href="#installation"><b>Installation</b></a>&nbsp;&bull;\n  <a href="#usage"><b>Usage</b></a>&nbsp;&bull;\n  <a href="#compatibility"><b>Compatibility</b></a>&nbsp;&bull;\n  <a href="#documentation"><b>Documentation</b></a>&nbsp;&bull;\n  <a href="#contribute"><b>Contribute</b></a>\n</p>\n\n<p align="center">\n  <a href="https://www.buymeacoffee.com/Q9C1Hnm28" target="_blank">\n    <img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee" />\n  </a>\n</p>\n\n\n# Synopsis\n\nThe `austin-python` package is a Python wrapper around the [Austin] binary that\nprovides convenience classes to quickly develop your statistical profiling\ntools. Whether your code is thread-based or asynchronous, `austin-python` has\nyou covered. This is, for instance, how you would turn Austin into a Python\napplication:\n\n~~~ python\nfrom austin.aio import AsyncAustin\n\n\n# Make your sub-class of AsyncAustin\nclass EchoAsyncAustin(AsyncAustin):\n    def on_ready(self, process, child_process, command_line):\n        print(f"Austin PID: {process.pid}")\n        print(f"Python PID: {child_process.pid}")\n        print(f"Command Line: {command_line}")\n\n    def on_sample_received(self, line):\n        print(line)\n\n    def on_terminate(self, data):\n        print(data)\n\n\n# Use the Proactor event loop on Windows\nif sys.platform == "win32":\n    asyncio.set_event_loop(asyncio.ProactorEventLoop())\n\ntry:\n    # Start the Austin application with some command line arguments\n    austin = EchoAsyncAustin()\n    asyncio.get_event_loop().run_until_complete(\n        austin.start(["-i", "10000", "python3", "myscript.py"])\n    )\nexcept (KeyboardInterrupt, asyncio.CancelledError):\n    pass\n~~~\n\nThe `austin-python` package is at the heart of the [Austin\nTUI](https://github.com/P403n1x87/austin-tui) and the [Austin\nWeb](https://github.com/P403n1x87/austin-web) Python applications. Go check them\nout if you are looking for full-fledged usage examples.\n\nIncluded with the package come two applications for the conversion of Austin\ncollected output, which is in the form of [collapsed\nstacks](https://github.com/brendangregg/FlameGraph), to either the\n[Speedscope](https://speedscope.app/) JSON format or the [Google pprof\nformat](https://github.com/google/pprof). Note, however, that the Speedscope web\napplication supports Austin native format directly.\n\n\n# Installation\n\nThis package can be installed from PyPI with\n\n~~~ bash\npip install --user austin-python --upgrade\n~~~\n\nPlease note that `austin-python` requires the [Austin] binary. The default\nlookup locations are, in order,\n\n- current working directory;\n- the `AUSTINPATH` environment variable which gives the path to the folder that\n  contains the Austin binary;\n- the `.austinrc` TOML configuration file in the user\'s home folder, e.g.\n  `~/.austinrc` on Linux (see below for a sample `.austinrc` file);\n- the `PATH` environment variable.\n\nA sample `.austinrc` file would look like so\n\n~~~ toml\nbinary = "/path/to/austin"\n~~~\n\n\n# Usage\n\nA simple example of an echo application was shown above. Other examples using,\ne.g., threads, can be found in the official documentation. You can also browse\nthrough the code of the [Austin TUI](https://github.com/P403n1x87/austin-tui)\nand the [Austin Web](https://github.com/P403n1x87/austin-web) Python\napplications to see how they leverage `austin-python`.\n\n## Format conversion\n\nAs it was mentioned before, this package also comes with two scripts for format\nconversion, namely `austin2speedscope` and `austin2pprof`. They both take two\nmandatory arguments, that is, the input and output file. For example, to convert\nthe Austin profile data file `myscript.aprof` to the Google pprof data file\n`myscript.pprof`, you can run\n\n~~~ bash\naustin2pprof myscript.aprof myscript.pprof\n~~~\n\nThe package also provide the `austin-compress` utility to compress the Austin\nraw samples by aggregation.\n\n# Compatibility\n\nThe `austin-python` package is tested on Linux, macOS and Windows with Python\n3.6-3.9.\n\n\n# Documentation\n\nThe official documentation is hosted on readthedocs.io at\n[austin-python.readthedocs.io](https://austin-python.readthedocs.io/).\n\n\n# Contribute\n\nIf you want to help with the development, then have a look at the open issues\nand have a look at the [contributing guidelines](CONTRIBUTING.md) before you\nopen a pull request.\n\nYou can also contribute to the development by either [becoming a\nPatron](https://www.patreon.com/bePatron?u=19221563) on Patreon, by [buying me a\ncoffee](https://www.buymeacoffee.com/Q9C1Hnm28) on BMC or by chipping in a few\npennies on [PayPal.Me](https://www.paypal.me/gtornetta/1).\n\n<p align="center">\n  <a href="https://www.buymeacoffee.com/Q9C1Hnm28" target="_blank">\n    <img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png"\n         alt="Buy Me A Coffee" />\n  </a>\n</p>\n\n\n[Austin]: https://github.com/p403n1x87/austin\n',
    'author': 'Gabriele N. Tornetta',
    'author_email': 'phoenix1987@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/P403n1x87/austin-python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
