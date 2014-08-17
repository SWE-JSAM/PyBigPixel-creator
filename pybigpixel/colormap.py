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

from PyQt5.QtWidgets import (QDialog, QApplication, QComboBox, QVBoxLayout,
                             QDialogButtonBox, QLabel, QGridLayout)
import sys
from PyQt5.QtCore import pyqtSignal


COLORMAPS = {'8-Colors': ((255, 0, 0), (0, 0, 255), (0, 255, 0), (255, 255, 0),
                          (255, 0, 255), (0, 255, 255), (0, 0, 0),
                          (255, 255, 255)),
             '5-Colors': ((255, 0, 0), (0, 0, 255), (0, 255, 0), (0, 0, 0),
                          (255, 255, 255)),
             'All': None,
             'Black-White': ((0, 0, 0), (255, 255, 255)),
             '6-Gray': ((0, 0, 0), (255, 255, 255), (50, 50, 50),
                        (100, 100, 100), (150, 150, 150), (25, 25, 25))}


class ColorMap(QDialog):
    color_map_changed = pyqtSignal()

    def __init__(self, settings_dict):
        super(ColorMap, self).__init__()
        self.settings = settings_dict
        self.ui()

    def ui(self):
        select_label = QLabel(self.tr("Chose color map"))
        self.select = QComboBox()
        self.select.addItems(sorted(COLORMAPS.keys()))
        self.select.setCurrentIndex(self.select.
                                    findText(self.settings['color_map']))

        layout = QGridLayout()
        layout.addWidget(select_label, 0, 0)
        layout.addWidget(self.select, 0, 2)

        button_layout = QVBoxLayout()
        buttonbox = QDialogButtonBox(QDialogButtonBox.Apply |
                                     QDialogButtonBox.Cancel)
        button_layout.addStretch()
        button_layout.addWidget(buttonbox)

        layout.addLayout(button_layout, 2, 1, 1, 2)

        self.setLayout(layout)
        self.setWindowTitle(self.tr('Select color map'))
        buttonbox.rejected.connect(self.close)
        buttonbox.button(QDialogButtonBox.Apply).clicked.connect(self.apply)

    def apply(self):
        if self.settings['color_map'] != self.select.currentText():
            self.settings['color_map'] = self.select.currentText()
            self.color_map_changed.emit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    test_dict = {'color_map': 'All'}
    win = ColorMap(test_dict)
    win.show()
    sys.exit(app.exec_())
