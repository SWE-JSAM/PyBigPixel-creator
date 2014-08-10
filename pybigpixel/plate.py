#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
# along with PyBigPixel Creator. If not, see
# <http://www.gnu.org/licenses/gpl.html>.
import math

'''
This module transfer the image files to bigpixel files.
'''

from PIL import (Image, ImageDraw)
from PIL.ImageQt import ImageQt


# TODO: The colors should be selected form available color maps/images
def _pix_color(pixel_data, color_plallet=None):
    # This function returns the pixel color
    if len(pixel_data) == 4 and pixel_data[3] == 0:
        return (255, 255, 255)
    elif color_plallet:
        return _closes_color(pixel_data, color_plallet)
    else:
        return (pixel_data[0], pixel_data[1], pixel_data[2])


def _closes_color(pix_color, color_pallet):
    # closes color will find a color closest to the pixel data

    dist = []
    for color in color_pallet:
        dist.append(math.sqrt(((pix_color[0] - color[0]) * 0.3) ** 2 +
                               ((pix_color[1] - color[1]) * 0.59) ** 2 +
                               ((pix_color[2] - color[2]) * 0.11) ** 2))
    return color_pallet[dist.index(min(dist))]


class PixDrawing():
    """
    This class makes the pattern
    """
    def __init__(self):
        self.pixels_tot = [30, 30]
        self.startImageName = None
        self.plateImage = None
        self.shape = 'squares'
        self.background = 'gray'
        self.pallet = None

    def load_image(self, image_name):
        self.startImageName = image_name
        self.start_image = Image.open(self.startImageName)

    def _topcentercrop(self, image):
        width, height = image.size
        if width / height != self.pixels_tot[0] / self.pixels_tot[1]:
        # find how to crop image
            if width / height > self.pixels_tot[0] / self.pixels_tot[1]:
                scale_width = int(height * self.pixels_tot[0] /
                                  self.pixels_tot[1])
                scale_height = height
                pad_left = int((width - scale_width) / 2)
                pad_right = width - scale_width - pad_left
                box_size = (pad_left, 0, width - pad_right, scale_height)
            else:
                scale_width = width
                scale_height = int(width * self.pixels_tot[1] /
                                   self.pixels_tot[0])
                box_size = (0, 0, scale_width, scale_height)
        else:
            box_size = (0, 0, width, height)
        return image.crop(box_size)

    def _make_pix_drawing(self, crop):
        image_out = Image.new('RGB', (self.pixels_tot[0] * 20,
                                      self.pixels_tot[1] * 20),
                              color=self.background)

        draw = ImageDraw.Draw(image_out)
        pix_fig = crop.resize(self.pixels_tot)
        step = 20

        if self.shape == 'circles':
            radius = 9

            for x_pix in range(self.pixels_tot[0]):
                for y_pix in range(self.pixels_tot[1]):
                    x = x_pix * step + step / 2
                    y = y_pix * step + step / 2

                    draw.ellipse((x - radius, y - radius, x +
                                  radius, y + radius),
                                 fill=_pix_color(pix_fig.getpixel((x_pix,y_pix)),
                                                 self.pallet))

        elif self.shape == 'squares':
            pix = step - 2
            for x_pix in range(self.pixels_tot[0]):
                for y_pix in range(self.pixels_tot[1]):
                    x, y = x_pix * step + 1, y_pix * step + 1
                    draw.rectangle((x, y, x + pix, y + pix),
                                   fill=_pix_color(pix_fig.getpixel((x_pix, y_pix)),
                                                   self.pallet))

        elif self.shape == 'filled squares':
            for x_pix in range(self.pixels_tot[0]):
                for y_pix in range(self.pixels_tot[1]):
                    x, y = x_pix * step + 1, y_pix * step + 1
                    draw.rectangle((x, y, x + step, y + step),
                                   fill=_pix_color(pix_fig.getpixel((x_pix, y_pix)),
                                                   self.pallet))

        elif self.shape == 'cross':
            for x_pix in range(self.pixels_tot[0]):
                for y_pix in range(self.pixels_tot[1]):
                    x = x_pix * step
                    y = y_pix * step
                    draw.line([x + 2, y + 2, x + step - 2, y + step - 2],
                              fill=_pix_color(pix_fig.getpixel((x_pix, y_pix)),
                                              self.pallet), width=3)
                    draw.line([x - 2 + step, y + 2, x + 2, y + step - 2],
                              fill=_pix_color(pix_fig.getpixel((x_pix, y_pix)),
                                              self.pallet), width=3)
        del pix_fig
        image_out.show()  # to test
        image_out = ImageQt(image_out)
        return image_out

    def generate_pix_drawing(self):
        crop = self._topcentercrop(self.start_image)
        self.pix_img = self._make_pix_drawing(crop)


if __name__ == '__main__':
    plate = PixDrawing()
    plate.pixels_tot = [40, 40]
    plate.pallet = ((255, 0, 0), (0, 0, 255), (0, 255, 0), (255, 255, 255),
                    (255, 255, 0), (255, 0, 255), (0, 255, 255), (0, 0, 0))
    plate.load_image('test.jpg')
    plate.generate_pix_drawing()
