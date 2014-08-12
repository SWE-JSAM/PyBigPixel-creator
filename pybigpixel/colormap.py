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
from PyQt5.QtWidgets import (QDialog, QApplication, QComboBox, QHBoxLayout,
    QVBoxLayout, QDialogButtonBox)
import sys


class ColorMap(QDialog):
    def __init__(self):
        super(ColorMap, self).__init__()
        self.ui()

    def ui(self):
        select = QComboBox()
        select.addItems(('None', 'color'))

        layout = QHBoxLayout()
        layout.addWidget(select)

        button_layout = QVBoxLayout()
        buttonbox = QDialogButtonBox(QDialogButtonBox.Apply |
                                     QDialogButtonBox.Cancel)
        button_layout.addStretch()
        button_layout.addWidget(buttonbox)
        layout.addLayout(button_layout)
        self.setLayout(layout)
        self.setWindowTitle(self.tr('Select color map'))
        buttonbox.rejected.connect(self.close)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = ColorMap()
    win.show()
    sys.exit(app.exec_())
