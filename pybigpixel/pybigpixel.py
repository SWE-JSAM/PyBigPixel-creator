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
from PyQt5.QtCore import (pyqtSignal, Qt, QLocale, QTranslator)
from PyQt5.QtWidgets import (QApplication, QMainWindow, QAction, QMenuBar,
                             QHBoxLayout, QLabel, QWidget, QFrame, QFileDialog,
                             QDialog, QTextBrowser, QPushButton, QVBoxLayout,
                             QDialogButtonBox, QGridLayout, QSpinBox,
                             QMessageBox, QSizePolicy, qApp, QComboBox)
from PyQt5.QtPrintSupport import (QPrintDialog, QPrinter)
from PIL import (Image)
from . import plate
from . import prepare
from colormap import ColorMap, COLORMAPS

__version__ = "0.2.2"


class Window(QMainWindow):

    def __init__(self, conf):
        super(Window, self).__init__()
        self.printer = QPrinter()
        self.window_title = "PyBigPixel Creator {0}".format(__version__)
        self.pixel = plate.PixDrawing()
        self.qpixmap_image = None
        self.qpixmap_pixel = None
        # all user settings in this dictionary
        self.settings_dict = {'shape': '',
                              'background': '',
                              'available_shapes': (self.tr('circles'),
                                                   self.tr('squares'),
                                                   self.tr('filled squares'),
                                                   self.tr('cross')),
                              'availible_backgrounds': (self.tr('gray'),
                                                        self.tr('white'),
                                                        self.tr('red'),
                                                       self.tr('blue'),
                                                       self.tr('green'),
                                                       self.tr('black')),
                              'pixels': [],
                              'lang': '',
                              'color_map': ''}

        self.color = ('gray', 'white', 'red', 'blue', 'green', 'black')
        self.shapes = ('circles', 'squares', 'filled squares', 'cross')
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.inImage_name = os.path.join(self.base_dir, 'data', 'images',
                                         'start_background.png')
        self.config_file = conf
        self.configure_get()
        self.ui()
        self.load_file()
        self.dirty = False

    def configure_get(self):
        # Load settings from configuration file
        data = self.config_file.read_config()
        shape, background, width_pixels, height_pixels, lang, _, color_map = data
        self.settings_dict['pixels'] = [width_pixels, height_pixels]

        back_ind = self.color.index(background)
        self.settings_dict['background'] = self.settings_dict['availible_backgrounds'][back_ind]

        shape_ind = self.shapes.index(shape)
        self.settings_dict['shape'] = self.settings_dict['available_shapes'][shape_ind]
        self.settings_dict['lang'] = lang
        self.settings_dict['color_map'] = color_map

    def ui(self):
        menubar = QMenuBar()
        menubar.setNativeMenuBar(True)  # make the menu bar OS specific

        bar_file = menubar.addMenu(self.tr("&File"))

        file_load = QAction(self.tr("&Load image"), self,
                            shortcut=QKeySequence.New,
                            statusTip=self.tr("Load a new image"),
                            triggered=self.open_file)

        file_save = QAction(self.tr("&Save plate"), self,
                            shortcut=QKeySequence.Save,
                            statusTip=self.tr("Save the pattern"),
                            triggered=self.save_file)

        file_print = QAction(self.tr("&Print"), self,
                             shortcut=QKeySequence.Print,
                             statusTip=self.tr("Print pixel pattern"),
                             triggered=self.print_file)

        file_settings_general = QAction(self.tr("S&ettings"), self,
                                        statusTip=self.tr('Change settings'),
                                        triggered=self.change_settings)

        file_settings_color = QAction(self.tr("Color map"), self,
                                      statusTip=self.tr('Define color map'),
                                      triggered=self.change_settings_color)

        file_quit = QAction(self.tr("&Quit"), self, shortcut=QKeySequence.Quit,
                            statusTip=self.tr('Quit the program'),
                            triggered=self.close)

        bar_file.addAction(file_load)
        bar_file.addAction(file_save)
        bar_file.addAction(file_print)
        bar_file.addAction(file_settings_general)
        bar_file.addAction(file_settings_color)
        bar_file.addAction(file_quit)

        bar_about = menubar.addMenu(self.tr("&About"))
        about_about = QAction(self.tr("&About"), self,
                              statusTip=self.tr("Show about PyBigPix"),
                              triggered=self.show_about)

        about_licence = QAction(self.tr("&License"), self,
                                statusTip=self.tr('Show license'),
                                triggered=self.show_license)

        about_QT = QAction(self.tr("About &QT"), self,
                           statusTip=self.tr("Show about QT"),
                           triggered=qApp.aboutQt)

        bar_about.addAction(about_about)
        bar_about.addAction(about_licence)
        bar_about.addAction(about_QT)

        self.setMenuWidget(menubar)
        self.setMenuBar(menubar)

        self.setWindowTitle(self.window_title)

        self.label_image = QLabel(self.tr("Start Image"))
        self.label_image.setSizePolicy(QSizePolicy.Expanding,
                                       QSizePolicy.Expanding)
        self.label_image.setMinimumSize(400, 400)
        self.label_image.textFormat()
        self.label_image.setFrameShape(QFrame.Panel)
        self.label_image.setAlignment(Qt.AlignCenter)

        self.lable_pixels = QLabel(self.tr("Pixel Image"))
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
        filename, _ = QFileDialog.getOpenFileNames(self, self.tr("Open Images"),
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
            QMessageBox.warning(self, self.tr("Save Error!"),
                                self.tr("No image present. Load an image first"))

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

    def change_config(self):
        color_index = self.settings_dict['availible_backgrounds'].index(self.settings_dict['background'])
        shape_index = self.settings_dict['available_shapes'].index(self.settings_dict['shape'])
        shape = self.shapes[shape_index]
        width, height = self.settings_dict['pixels']
        back_color = self.color[color_index]
        lang = self.settings_dict['lang']
        color_map = self.settings_dict['color_map']
        self.config_file.write_config(shape, back_color,  str(width),
                                      str(height), lang, __version__,
                                      color_map)

    def change_settings(self):
        settings = Settings(self.settings_dict, self)
        settings.changed.connect(self.refresh_plate)
        settings.changed.connect(self.change_config)
        settings.langchanged.connect(self.change_lang)
        settings.show()

    # TODO: This function should make i possible to select predefined color
    # maps and make own color maps. The color maps should be saved in
    # configuration file
    def change_settings_color(self):
        cmap = ColorMap(self.settings_dict)
        cmap.color_map_changed.connect(self.refresh_plate)
        cmap.color_map_changed.connect(self.change_config)
        cmap.exec_()

    def change_lang(self):
        QMessageBox.information(self, 'Information', 'Restart the program, to '
                                        'activate languish changes')

    def close(self):
        if self.dirty:
            close_question = QMessageBox.question(self, "PyBigPixel Creator {0}",
                             self.tr(" -- Save Images"), format(__version__),
                             self.tr("File has unsaved changes.Save now?"),
                             QMessageBox.Yes | QMessageBox.No |
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
            color_index = self.settings_dict['availible_backgrounds'].index(self.settings_dict['background'])
            shape_index = self.settings_dict['available_shapes'].index(self.settings_dict['shape'])
            self.pixel.shape = self.shapes[shape_index]
            self.pixel.color_map['RGB'] = COLORMAPS[self.settings_dict['color_map']]
            self.pixel.pixels_tot = self.settings_dict['pixels']
            self.pixel.background = self.color[color_index]
            self.pixel.generate_pix_drawing()
            self.qpixmap_pixel = QPixmap.fromImage(self.pixel.pix_img)
            self.lable_pixels.setPixmap(self.qpixmap_pixel)
            self.updatescreensize()
        else:
            QMessageBox.warning(self, self.tr('Warning'),
                                self.tr("You need to first load an Image"))


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
    langchanged = pyqtSignal()

    def __init__(self, shape, parent=None):
        super(Settings, self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)
        # Make reference copy of variable
        self.shape = shape

        self.setWindowTitle("PyBigPixel Creator {0}-- {1}"
                            .format(__version__, self.tr('Settings')))

        lang_label = QLabel(self.tr("Languish"))
        self.lang_list = QComboBox()
        langs = [prepare.LANGUISH[key]['Lang'] for
                 key in prepare.LANGUISH.keys()]
        self.lang = shape['lang']
        self.lang_list.addItems(langs)
        self.lang_list.setCurrentIndex(self.lang_list.findText(self.lang))

        shape_label = QLabel(self.tr("Shape of pixel"))
        self.shape_list = QComboBox()
        self.shape_list.addItems(self.shape['available_shapes'])
        self.shape_list.setCurrentIndex(self.shape_list.
                                        findText(self.shape['shape']))

        plate_label = QLabel(self.tr("Number of pixels (width x height)"))
        plate_label_x = QLabel(" X ")
        self.pixel_button_width = QSpinBox()
        self.pixel_button_width.setRange(1, 250)
        self.pixel_button_width.setValue(self.shape['pixels'][0])

        self.pixel_button_height = QSpinBox()
        self.pixel_button_height.setRange(1, 250)
        self.pixel_button_height.setValue(self.shape['pixels'][1])

        self.background_label = QLabel(self.tr("Background color"))
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
        layout.addWidget(lang_label, 0, 0)
        layout.addWidget(self.lang_list, 0, 2, 1, 2)

        layout.addWidget(shape_label, 1, 0)
        layout.addWidget(self.shape_list, 1, 2, 1, 2)

        layout.addWidget(self.background_label, 2, 0)
        layout.addWidget(self.background_list, 2, 2, 1, 2)

        layout.addWidget(plate_label, 3, 0)
        layout.addWidget(self.pixel_button_width, 3, 1, 1, 1)
        layout.addWidget(plate_label_x, 3, 2)
        layout.addWidget(self.pixel_button_height, 3, 3, 1, 1)

        layout.addLayout(button_layout, 4, 0, 2, 4)
        self.setLayout(layout)

        buttonbox.rejected.connect(self.close)
        buttonbox.button(QDialogButtonBox.Apply).clicked.connect(self.apply)

    def apply(self):
        self.shape['pixels'][0] = self.pixel_button_width.value()
        self.shape['pixels'][1] = self.pixel_button_height.value()
        self.shape['shape'] = self.shape_list.currentText()
        self.shape['background'] = self.background_list.currentText()
        if self.lang_list.currentText() != self.lang:
            self.shape['lang'] = self.lang_list.currentText()
            self.langchanged.emit()
        self.changed.emit()


def main():
    app = QApplication(sys.argv)
    locale = QLocale.system().name()
    conf = prepare.Config()
    local_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                             'data', 'locale'))
    translator = QTranslator()

    if not os.path.isfile(conf.config_file):
        if locale in prepare.LANGUISH.keys():
            conf.write_config('squares', 'gray', 30, 30,
                              prepare.LANGUISH[locale]['Lang'], __version__,
                              'All')
            translator.load(os.path.join(local_dir, 'pybigpixel_' +
                                         locale + '.qm'))
            app.installTranslator(translator)

        else:
            conf.write_config('squares', 'gray', 30, 30, 'English',
                              __version__, 'All')

    else:
        key = [key for key in prepare.LANGUISH.keys() if
               prepare.LANGUISH[key]['Lang'] == conf.get_languish()]

        if key[0] != 'default':
            translator.load(os.path.join(local_dir, 'pybigpixel_' +
                                         key[0] + '.qm'))
            app.installTranslator(translator)

    window = Window(conf)
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
