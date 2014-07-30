# Authors: Jörgen Samuelsson <samuelssonjorgen@gmail.com>
# PyBigPixel Creator software converts your digital images to pixel patterns.
#
# PyBigPixel Creator is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PyBigPixel Creator is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PyBigPixel Creator. If not, see <http://www.gnu.org/licenses/gpl.html>.


import os
import re
from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

def add_data():
    try:
        data_files = [('share/applications', ['extra/pybigpixel.desktop']),
                ('share/pixmaps', ['extra/pybigpixel.svg'])]
        return data_files
    except:
        return

package_version = re.search('__version__ = "*.*.*"',
        open(os.path.join('pybigpixel', 'pybigpixel.py'))
        .read()).group().split('"')[1]
 
if os.name == 'posix':
    data_files = add_data()
else:
    data_files = None

setup(
    name = 'pybigpixel creator',
    version = package_version,
    author='Jörgen Samuelsson',
    author_email='samuelssonjorgen@gmail.com',
    install_requires=['setuptools', 'Pillow'],
    url = 'https://github.com/SWE-JSAM/PyBigPixel-creator',
    description = 'The program converts your digital images to pixel patterns',
    long_description=long_description,
    license='GPLv3',
    packages = ['pybigpixel'],
    include_package_data=True,
    data_files=data_files,
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: X11 Applications :: QT',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Multimedia :: Graphics',
        'Topic :: Multimedia :: Graphics :: Graphics Conversion',
    ],
    entry_points={
        'gui_scripts': [
            'pybigpixel = pybigpixel.pybigpixel:main',
            ]
        },
)
