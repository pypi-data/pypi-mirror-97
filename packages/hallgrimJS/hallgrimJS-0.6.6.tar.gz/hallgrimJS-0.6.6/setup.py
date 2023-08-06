# -*- coding: utf-8 -*-

from setuptools import setup

import re

with open('hallgrimJS/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

long_description = """
The final data is produced in three steps:

1. A python script file with predefined structure that has to export certain variables in a specified format.
2. An intermediate representation (probably an array that contains relevant data and assumes unknown properties)
3. The XML structure for one or multiple questions, readable by Ilias.
4. An Ilias object packed as .zip file, ready for upload.
"""

setup(
    name='hallgrimJS',
    version=version,
    description='A script generator for the ILIAS platform',
    long_description=long_description,
    author='Jan Maximilian Michal, Lukas Mayer, Toni Ringling',
    author_email='t.ringling@gmx.net',
    url='https://gitlab.gwdg.de/lukas.mayer/ilias-generator',
    download_url = 'https://gitlab.gwdg.de/lukas.mayer/ilias-generator/repository/archive.tar.gz?ref=%s' % version,
    license='MIT',
    scripts=['bin/hallgrimJS'],
    install_requires=['mistune>=0.7', 'pygments>=2', 'requests>=2.8', 'asciitomathml>=1.0', 'lxml', 'rjsmin>=1.1.0'],
    packages=[
        'hallgrimJS',
        'hallgrimJS.IliasXMLCreator',
        'hallgrimJS.xsl_yarosh',
        'hallgrimJS.GraphNodePics'],
    package_data={'hallgrimJS.xsl_yarosh': ['*.xsl', 'README'],
                  'hallgrimJS': ['*.js', '*.pdf'],
                  'hallgrimJS.GraphNodePics': ['*.png']}
)
