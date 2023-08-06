#!/usr/bin/env python

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
        name = 'pypi-cleanup',
        version = '0.1.0',
        description = '# PyPI Bulk Release Version Cleanup Utility',
        long_description = '# PyPI Bulk Release Version Cleanup Utility\n\n[![PyPI Cleanup Version](https://img.shields.io/pypi/v/pypi-cleanup?logo=pypi)](https://pypi.org/project/pypi-cleanup/)\n[![PyPI Cleanup Python Versions](https://img.shields.io/pypi/pyversions/pypi-cleanup?logo=pypi)](https://pypi.org/project/pypi-cleanup/)\n[![PyPI Cleanup Downloads Per Day](https://img.shields.io/pypi/dd/pypi-cleanup?logo=pypi)](https://pypi.org/project/pypi-cleanup/)\n[![PyPI Cleanup Downloads Per Week](https://img.shields.io/pypi/dw/pypi-cleanup?logo=pypi)](https://pypi.org/project/pypi-cleanup/)\n[![PyPI Cleanup Downloads Per Month](https://img.shields.io/pypi/dm/pypi-cleanup?logo=pypi)](https://pypi.org/project/pypi-cleanup/)\n\n## Overview\n\nPyPI Bulk Release Version Cleanup Utility (`pypi-cleanup`) is designed to bulk-delete releases from PyPI that match\nspecified patterns.\nThis utility is most useful when CI/CD method produces a swarm of temporary\n[.devN pre-releases](https://www.python.org/dev/peps/pep-0440/#developmental-releases) in between versioned releases.\n\nBeing able to cleanup past .devN junk helps PyPI cut down on the storage requirements and keeps release history neatly\norganized.\n\n## WARNING\n\nTHIS UTILITY IS DESTRUCTIVE AND CAN POTENTIALLY WRECK YOUR PROJECT RELEASES AND MAKE THE PROJECT INACCESSIBLE ON PYPI.\n\nThis utility is provided on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or\nimplied, including, without limitation, any warranties or conditions of TITLE, NON-INFRINGEMENT, MERCHANTABILITY,\nor FITNESS FOR A PARTICULAR PURPOSE.\n\n## Details\n\nThe default package release version selection pattern is `r".*dev\\d+$"`.\n\nAuthentication password may be passed via environment variable\n`PYPI_CLEANUP_PASSWORD`. Otherwise, you will be prompted to enter it.\n\nAuthentication with TOTP is supported.\n\nExamples:\n\n```bash\n$ pypi-cleanup --help\nusage: pypi-cleanup [-h] -u USERNAME -p PACKAGE [-t URL] [-r PATTERNS] [-n] [-y] [-v]\n\nPyPi Package Cleanup Utility\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -u USERNAME, --username USERNAME\n                        authentication username (default: None)\n  -p PACKAGE, --package PACKAGE\n                        PyPI package name (default: None)\n  -t URL, --host URL    PyPI <proto>://<host> prefix (default: https://pypi.org/)\n  -r PATTERNS, --version-regex PATTERNS\n                        regex to use to match package versions to be deleted (default: None)\n  -n, --dry-run         do not actually delete anything (default: False)\n  -y, --yes             confirm dangerous action (default: False)\n  -v, --verbose         be verbose (default: 0)\n```\n\n```bash\n$ pypi-cleanup -u arcivanov -p pybuilder\nPassword: \nAuthentication code: 123456\nINFO:root:Deleting pybuilder version 0.12.3.dev20200421010849\nINFO:root:Deleted pybuilder version 0.12.3.dev20200421010849\nINFO:root:Deleting pybuilder version 0.12.3.dev20200421010857\nINFO:root:Deleted pybuilder version 0.12.3.dev20200421010857\n```\n\n```bash\n$ pypi-cleanup -u arcivanov -p geventmp -n -r \'.*\\\\.dev1$\'\nPassword:\nWARNING:root:RUNNING IN DRY-RUN MODE\nINFO:root:Will use the following patterns [re.compile(\'.*\\\\.dev1$\')] on package geventmp\nAuthentication code: 123456\nINFO:root:Deleting geventmp version 0.0.1.dev1\n```',
        long_description_content_type = 'text/markdown',
        author = 'Arcadiy Ivanov',
        author_email = 'arcadiy@ivanov.biz',
        license = 'Apache License, Version 2.0',
        url = 'https://github.com/arcivanov/pypi-cleanup',
        scripts = [],
        packages = ['pypi_cleanup'],
        namespace_packages = [],
        py_modules = [],
        classifiers = [
            'Programming Language :: Python',
            'Programming Language :: Python :: Implementation :: CPython',
            'Programming Language :: Python :: Implementation :: PyPy',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Operating System :: MacOS :: MacOS X',
            'Operating System :: POSIX :: Linux',
            'Operating System :: Microsoft :: Windows',
            'Operating System :: OS Independent',
            'Development Status :: 5 - Production/Stable',
            'Environment :: Console',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: Apache Software License',
            'Topic :: Software Development :: Build Tools'
        ],
        entry_points = {
            'console_scripts': ['pypi-cleanup = pypi_cleanup:main']
        },
        data_files = [],
        package_data = {
            'pypi_cleanup': ['LICENSE']
        },
        install_requires = ['requests~=2.23'],
        dependency_links = [],
        zip_safe = True,
        cmdclass = {'install': install},
        keywords = 'PyPI cleanup build dev tool release version',
        python_requires = '>=3.6',
        obsoletes = [],
    )
