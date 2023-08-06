#!/usr/bin/env python

from setuptools import setup, Extension
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
        name = 'pybuilder-setup-cfg',
        version = '0.0.7',
        description = 'PyBuilder plugin for getting information from setup.cfg file or environment variables',
        long_description = '\nPlease, see https://github.com/margru/pybuilder-setup-cfg for more information.\n',
        author = 'Martin Gruber',
        author_email = 'martin.gruber@email.cz',
        license = 'MIT',
        url = 'https://github.com/margru/pybuilder-setup-cfg',
        scripts = [],
        packages = ['pybuilder_setup_cfg'],
        namespace_packages = [],
        py_modules = [],
        ext_modules = [] + [],
        classifiers = [
            'Development Status :: 3 - Alpha',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 2.7'
        ],
        entry_points = {},
        data_files = [],
        package_data = {},
        include_package_data = False,
        install_requires = ['configparser'],
        dependency_links = [],
        zip_safe = True,
        cmdclass = {'install': install},
        keywords = '',
        python_requires = '',
        obsoletes = [],
    )
