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

import sys
import os

from PyQt5.QtGui import (QPixmap, QPainter, QTransform, QKeySequence)
from PyQt5.QtCore import (pyqtSignal, Qt)
from PyQt5.QtWidgets import (QApplication, QMainWindow, QAction, QMenuBar,
                             QHBoxLayout, QLabel, QWidget, QFrame, QFileDialog,
                             QDialog, QTextBrowser, QPushButton, QVBoxLayout,
                             QDialogButtonBox, QGridLayout, QSpinBox,
                             QMessageBox, QSizePolicy, qApp, QComboBox)
from PyQt5.QtPrintSupport import (QPrintDialog, QPrinter)
from PIL import (Image)
from . import plate

__version__ = "0.1.5"


class Window(QMainWindow):

    def __init__(self):
        super(Window, self).__init__()
        self.printer = QPrinter()
        self.window_title = "PyBigPixel Creator {0}".format(__version__)
        self.pixel = plate.PixDrawing()
        self.qpixmap_image = None
        self.qpixmap_pixel = None
        # all user settings in this dictionary
        self.settings_dict = {'shape': 'squares',
                              'background': 'gray',
                              'available_shapes': ('circles', 'squares',
                                                   'filled squares', 'cross'),
                              'availible_backgrounds': ('gray', 'white', 'red',
                                                       'blue', 'green',
                                                       'black'),
                              'pixels': [30, 30]}

        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.inImage_name = os.path.join(self.base_dir, 'data', 'images',
                                         'start_background.png')

        self.ui()
        self.load_file()
        self.dirty = False

    def ui(self):
        menubar = QMenuBar()
        menubar.setNativeMenuBar(True)  # make the menu bar OS specific

        bar_file = menubar.addMenu("&File")

        file_load = QAction("&Load image", self, shortcut=QKeySequence.New,
                            statusTip="Load a new image",
                            triggered=self.open_file)

        file_save = QAction("&Save plate", self, shortcut=QKeySequence.Save,
                            statusTip="Save the pattern",
                            triggered=self.save_file)

        file_print = QAction("&Print", self, shortcut=QKeySequence.Print,
                            statusTip="Print pixel pattern",
                            triggered=self.print_file)

        file_settings = QAction("S&ettings", self, statusTip='Change settings',
                                triggered=self.change_settings)

        file_quit = QAction("&Quit", self, shortcut=QKeySequence.Quit,
                            statusTip='Quit the program',
                            triggered=self.close)

        bar_file.addAction(file_load)
        bar_file.addAction(file_save)
        bar_file.addAction(file_print)
        bar_file.addAction(file_settings)
        bar_file.addAction(file_quit)

        bar_about = menubar.addMenu("&About")
        about_about = QAction("&About", self, statusTip="Show about PyBigPix",
                              triggered=self.show_about)

        about_licence = QAction("&License", self, statusTip='Show license',
                                triggered=self.show_license)

        about_QT = QAction("About &QT", self, statusTip="Show about QT",
                           triggered=qApp.aboutQt)

        bar_about.addAction(about_about)
        bar_about.addAction(about_licence)
        bar_about.addAction(about_QT)

        self.setMenuWidget(menubar)
        self.setMenuBar(menubar)

        self.setWindowTitle(self.window_title)

        self.label_image = QLabel("Start Image")
        self.label_image.setSizePolicy(QSizePolicy.Expanding,
                                       QSizePolicy.Expanding)
        self.label_image.setMinimumSize(400, 400)
        self.label_image.textFormat()
        self.label_image.setFrameShape(QFrame.Panel)
        self.label_image.setAlignment(Qt.AlignCenter)

        self.lable_pixels = QLabel("Pixel Image")
        self.lable_pixels.setMinimumSize(400, 400)
        self.lable_pixels.setSizePolicy(QSizePolicy.Expanding,
                                       QSizePolicy.Expanding)
        self.lable_pixels.setAlignment(Qt.AlignCenter)
        self.lable_pixels.setFrameShape(QFrame.Panel)

        self.centeralwidget = QWidget()
        layout = QHBoxLayout(self.centeralwidget)
        layout.addWidget(self.label_image)
        layout.addWidget(self.lable_pixels)
        self.setCentralWidget(self.centeralwidget)

    def resizeEvent(self, event):
        scaledSize = self.label_image.size()
        scaledSize.scale(self.label_image.size(), Qt.KeepAspectRatio)
        if (self.qpixmap_image != None and
            self.qpixmap_image.size() != scaledSize):
            self.updatescreensize()

    def updatescreensize(self):
        self.label_image.setPixmap(self.qpixmap_image.scaled
                                   (self.label_image.size(),
                                    Qt.KeepAspectRatio,
                                    Qt.SmoothTransformation))

        self.lable_pixels.setPixmap(self.qpixmap_pixel.scaled
                                   (self.lable_pixels.size(),
                                    Qt.KeepAspectRatio,
                                    Qt.SmoothTransformation))

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileNames(self, "Open Images",
                                                   os.path.expanduser("~"),
                                                  "Images (*.png *.jpg *.bmp"
                                                  " *.tif);;All Files (*)")
        # to handle cancel option
        if filename:
            self.inImage_name = filename[0]
            self.load_file()
        else:
            pass

    def load_file(self):
        self.pixel.start_image = Image.open(self.inImage_name)
        self.qpixmap_image = QPixmap(self.inImage_name)
        self.label_image.setPixmap(self.qpixmap_image)
        self.refresh_plate()
        self.window_title = "PyBigPixel Creator {0} -- Untitled pattern".format(__version__)
        self.setWindowTitle(self.window_title)
        self.dirty = True
        self.updatescreensize()

    def save_file(self):
        if self.inImage_name:
            title = "PyBigPixel Creator {0} -- Save Images".format(__version__)
            saveFileName = QFileDialog.getSaveFileName(self, title, '', ".bmp")
            if ".bmp" in saveFileName:
                file = saveFileName[0]
            else:
                file = saveFileName[0] + saveFileName[1]

            self.pixel.pix_img.save(file)
            self.dirty = False
            self.window_title = "PyBigPixel Creator {0} -- {1}".format(__version__, file[:-4].split('/')[-1])
            self.setWindowTitle(self.window_title)
        else:
            QMessageBox.warning(self, "Save Error!",
                                "No image present. Load an image first")

    def print_file(self):
        dialog = QPrintDialog(self.printer, self)
        if dialog.exec_():
            painter = QPainter(self.printer)
            rect = painter.viewport()
            # auto landscape or portrait printing depending on picture
            if self.qpixmap_pixel.width() > self.qpixmap_pixel.height():
                self.qpixmap_pixel = self.qpixmap_pixel.transformed(QTransform().rotate(90))
            size = self.qpixmap_pixel.size()
            size.scale(rect.size(), Qt.KeepAspectRatio)
            painter.setViewport(rect.x(), rect.y(), size.width(),
                                size.height())
            painter.setWindow(self.qpixmap_pixel.rect())
            painter.drawPixmap(0, 0, self.qpixmap_pixel)

    def change_settings(self):
        settings = Settings(self.settings_dict, self)
        settings.changed.connect(self.refresh_plate)
        settings.show()

    def close(self):
        if self.dirty:
            close_question = QMessageBox.question(self, "PyBigPixel Creator {0}"
                                                       " -- Save Images"
                                                       .format(__version__),
                                                  "File has unsaved changes."
                                                  " Save now?",
                                                  QMessageBox.Yes |
                                                  QMessageBox.No |
                                                  QMessageBox.Cancel)
            if close_question == QMessageBox.Yes:
                self.save_file()
            elif close_question == QMessageBox.No:
                QWidget.close(self)
            elif close_question == QMessageBox.Cancel:
                pass
        else:
            QWidget.close(self)

    def show_about(self):
        about = AbouteInfo(os.path.join(self.base_dir, 'data', 'text',
                                        'about.html'), 'About')
        about.exec_()

    def show_license(self):
        licence = AbouteInfo(os.path.join(self.base_dir, 'data', 'text',
                                          'gpl.html'), 'License')
        licence.exec_()

    def refresh_plate(self):
        self.dirty = True
        if ('Untitled' not in self.window_title
            and '*' not in self.window_title):
            self.window_title = self.window_title + '*'
            self.setWindowTitle(self.window_title)

        if self.inImage_name:
            # load all data from the user settings to plate module
            self.pixel.load_image(self.inImage_name)
            self.pixel.shape = self.settings_dict['shape']
            self.pixel.pixels_tot = self.settings_dict['pixels']
            self.pixel.background = self.settings_dict['background']
            self.pixel.generate_pix_drawing()
            self.qpixmap_pixel = QPixmap.fromImage(self.pixel.pix_img)
            self.lable_pixels.setPixmap(self.qpixmap_pixel)
            self.updatescreensize()
        else:
            QMessageBox.warning(self, 'Warning',
                                "You need to first load an Image")


class AbouteInfo(QDialog):
    def __init__(self, htmlfile, name):
        super(AbouteInfo, self).__init__()
        self.text = QTextBrowser()
        text = open(htmlfile).read()
        self.text.setHtml(text)
        self.text.setOpenExternalLinks(True)
        self.cancelbutton = QPushButton("&Close")
        self.setGeometry(100, 100, 700, 700)
        buttonlayout = QHBoxLayout()
        buttonlayout.addStretch()
        buttonlayout.addWidget(self.cancelbutton)
        layout = QVBoxLayout()
        layout.addWidget(self.text)
        layout.addLayout(buttonlayout)
        self.setLayout(layout)
        self.setWindowTitle("PyBigPixel Creator {0}-- {1}".format(__version__, name))
        self.cancelbutton.clicked.connect(self.close)


class Settings(QDialog):
    changed = pyqtSignal()

    def __init__(self, shape, parent=None):
        super(Settings, self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)
        # Make reference copy of variables
        self.shape = shape
        self.setWindowTitle("PyBigPixel Creator {0}-- {1}"
                            .format(__version__, 'Settings'))

        shape_label = QLabel("Shape of pixel")
        self.shape_list = QComboBox()
        self.shape_list.addItems(self.shape['available_shapes'])
        self.shape_list.setCurrentIndex(self.shape_list.
                                        findText(self.shape['shape']))

        plate_label = QLabel("Number of PyBigPixel Creators"
                             "used (width x height)")
        plate_label_x = QLabel(" X ")
        self.pixel_button_width = QSpinBox()
        self.pixel_button_width.setRange(1, 250)
        self.pixel_button_width.setValue(self.shape['pixels'][0])

        self.pixel_button_height = QSpinBox()
        self.pixel_button_height.setRange(1, 250)
        self.pixel_button_height.setValue(self.shape['pixels'][1])

        self.background_label = QLabel("Background color")
        self.background_list = QComboBox()
        self.background_list.addItems(self.shape['availible_backgrounds'])
        self.background_list.setCurrentIndex(self.background_list.
                                             findText(self.shape['background']))

        button_layout = QVBoxLayout()
        buttonbox = QDialogButtonBox(QDialogButtonBox.Apply |
                                     QDialogButtonBox.Cancel)
        button_layout.addStretch()
        button_layout.addWidget(buttonbox)

        layout = QGridLayout()
        layout.addWidget(shape_label, 0, 0)
        layout.addWidget(self.shape_list, 0, 2, 1, 2)

        layout.addWidget(self.background_label, 1, 0)
        layout.addWidget(self.background_list, 1, 2, 1, 2)

        layout.addWidget(plate_label, 2, 0)
        layout.addWidget(self.pixel_button_width, 2, 1, 1, 1)
        layout.addWidget(plate_label_x, 2, 2)
        layout.addWidget(self.pixel_button_height, 2, 3, 1, 1)

        layout.addLayout(button_layout, 3, 0, 2, 4)
        self.setLayout(layout)

        buttonbox.rejected.connect(self.close)
        buttonbox.button(QDialogButtonBox.Apply).clicked.connect(self.apply)

    def apply(self):
        self.shape['pixels'][0] = self.pixel_button_width.value()
        self.shape['pixels'][1] = self.pixel_button_height.value()
        self.shape['shape'] = self.shape_list.currentText()
        self.shape['background'] = self.background_list.currentText()
        self.changed.emit()


def main():
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
