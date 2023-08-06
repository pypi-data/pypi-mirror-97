#!/usr/bin/env python
#   -*- coding: utf-8 -*-

from setuptools import setup
from setuptools.command.install import install as _install

class install(_install):
    def pre_install_script(self):
        pass

    def post_install_script(self):
        pass

    def run(self):
        self.pre_install_script()

        _install.run(self)

        self.post_install_script()

if __name__ == '__main__':
    setup(
        name = 'pybuilder-radon',
        version = '0.1.2',
        description = 'Pybuilder plugin for radon cyclomatic complexity',
        long_description = "[![GitHub Workflow Status](https://github.com/soda480/pybuilder-radon/workflows/build/badge.svg)](https://github.com/soda480/pybuilder-radon/actions)\n[![Code Coverage](https://codecov.io/gh/soda480/pybuilder-radon/branch/main/graph/badge.svg)](https://codecov.io/gh/soda480/pybuilder-radon)\n[![Code Grade](https://www.code-inspector.com/project/19887/status/svg)](https://frontend.code-inspector.com/project/19887/dashboard)\n[![PyPI version](https://badge.fury.io/py/pybuilder-radon.svg)](https://badge.fury.io/py/pybuilder-radon)\n\n# pybuilder-radon #\n\nA pybuilder plugin that checks the cyclomatic complexity of your project using `radon`. For more information about radon refer to the [radon pypi page](https://pypi.org/project/radon/).\n\nTo add this plugin into your pybuilder project, add the following line near the top of your build.py:\n```python\nuse_plugin('pypi:pybuilder_radon', '~=0.1.2')\n```\n\n**NOTE** version `v0.1.x` of this plugin will only work with version `v0.11.x` of Pybuilder.\n\n### cyclomatic complexity ###\n\nCyclomatic complexity is a software metric used to indicate the complexity of a program. It is a quantitative measure of the number of linearly independent paths through a program's source code. Cyclomatic complexity can be used to measure code complexity. The higher the complexity score the more complex the code, which typically translates to the code being more difficult to understand, maintain and to test. The number of the Cyclomatic complexity depends on how many different execution paths or control flow of your code can execute depending on various inputs. The metrics for Cyclomatic Complexity are:\n\nScore | Complexity | Risk Type\n-- | -- | --\n1 to 10 | simple | not much risk\n11 to 20 | complex | low risk\n21 to 50 | too complex | medium risk, attention\nmore than 50 | very complex | unable to test, high risk\n\nRefer to [cyclomatic complexity](https://www.c-sharpcorner.com/article/code-metrics-cyclomatic-complexity/) for more information.\n\n### Pybuilder radon properties ###\n\nThe pybuilder task `pyb radon` will use radon to to analyze your project and display the average cyclomatic complexity, verbose mode will display complexity of all classes, functions and methods analyzed. The following plugin properties are available to further configure the plugin's execution.\n\nName | Type | Default Value | Description\n-- | -- | -- | --\nradon_break_build_average_complexity_threshold | float | None | Fail build if overall average complexity is greater than the specified threshold\nradon_break_build_complexity_threshold | float | None | Fail build if complexity of any class, function or method exceeds the specified threshold\n\nThe plugin properties are set using `project.set_property`, for example setting the following properties, `pyb complexity` will fail if the average overall complexity score of the project exceeds `4` or if the complexity score of **any** class, method or function exceeds `10`:\n\n```Python\nproject.set_property('radon_break_build_average_complexity_threshold', 4)\nproject.set_property('radon_break_build_complexity_threshold', 10)\n```\n\n### Development ###\n\nClone the repository and ensure the latest version of Docker is installed on your development server.\n\nBuild the Docker image:\n```sh\ndocker image build \\\n-t \\\npybradon:latest .\n```\n\nRun the Docker container:\n```sh\ndocker container run \\\n--rm \\\n-it \\\n-v $PWD:/pybuilder-radon \\\npybradon:latest \\\n/bin/sh\n```\n\nExecute the build:\n```sh\npyb -X\n```",
        long_description_content_type = 'text/markdown',
        classifiers = [
            'Development Status :: 4 - Beta',
            'Environment :: Other Environment',
            'Environment :: Plugins',
            'Intended Audience :: Developers',
            'Intended Audience :: System Administrators',
            'License :: OSI Approved :: Apache Software License',
            'Operating System :: POSIX :: Linux',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3.6',
            'Topic :: Software Development :: Build Tools'
        ],
        keywords = '',

        author = 'Emilio Reyes',
        author_email = 'soda480@gmail.com',
        maintainer = '',
        maintainer_email = '',

        license = 'Apache License, Version 2.0',

        url = 'https://github.com/soda480/pybuilder-radon',
        project_urls = {},

        scripts = [],
        packages = ['pybuilder_radon'],
        namespace_packages = [],
        py_modules = [],
        entry_points = {},
        data_files = [],
        package_data = {},
        install_requires = ['radon'],
        dependency_links = [],
        zip_safe = True,
        cmdclass = {'install': install},
        python_requires = '',
        obsoletes = [],
    )
