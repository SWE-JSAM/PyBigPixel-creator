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

import configparser
import os

LANGUISH = {'sv_SE': {'Lang': 'Swedish', 'file': 'pybigpixel_sv_SE.qm'},
            'default': {'Lang': 'English', 'file': 'default'}}


class Config(object):
    """Read, write / create config file."""
    def __init__(self):
        config_dir = os.path.expanduser('~/.config')
        self.config_dir = os.path.join(config_dir, 'pybigpixel')
        if not os.path.isdir(self.config_dir):
            os.mkdir(self.config_dir)
        self.config_file = os.path.join(self.config_dir, 'pybigpixel.conf')

        self.config = configparser.ConfigParser()

    def read_config(self):
        self.config.read(self.config_file)
        com = self.config['Common']
        shape = str(com['shape'])
        background = str(com['background'])
        width_pixels = int(com['width_pixels'])
        height_pixels = int(com['height_pixels'])
        languish = str(com['languish'])
        version = str(com['version'])
        colormap = str(com['color_map'])
        return (shape, background, width_pixels, height_pixels, languish,
                version, colormap)

    def write_config(self, shape, background, width_pixels, height_pixels,
                     languish, version, color_map):
        self.config['Common'] = {}
        com = self.config['Common']
        com['shape'] = str(shape)
        com['background'] = str(background)
        com['width_pixels'] = str(width_pixels)
        com['height_pixels'] = str(height_pixels)
        com['languish'] = str(languish)
        com['version'] = str(version)
        com['color_map'] = str(color_map)
        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)

    def get_languish(self):
        self.config.read(self.config_file)
        com = self.config['Common']
        languish = str(com['languish'])
        return languish


if __name__ == '__main__':
    conf = Config()
    conf.write_config('squares', 'gray', '30', '30', 'Swedish', '0.2.2', 'None')
    print(conf.read_config())
