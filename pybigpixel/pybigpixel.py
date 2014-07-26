'''
PyBigPixel Creator software converts your digital images to pixel patterns.
'''
import sys
import os

from PyQt5.QtGui import (QPixmap, QPainter, QTransform)
from PyQt5.QtCore import (pyqtSignal, Qt)
from PyQt5.QtWidgets import (QApplication, QMainWindow, QAction, QMenuBar,
                             QHBoxLayout, QLabel, QWidget, QFrame, QFileDialog,
                             QDialog, QTextBrowser, QPushButton, QVBoxLayout,
                             QDialogButtonBox, QGridLayout, QSpinBox,
                             QMessageBox, QSizePolicy, qApp, QComboBox)
from PyQt5.QtPrintSupport import (QPrintDialog, QPrinter)
from PIL import (Image)
from plate import PixDrawing
_version = "0.1"


class Window(QMainWindow):

    def __init__(self):
        super(Window, self).__init__()
        self.printer = QPrinter()
        self.window_title = "PyBigPixel Creator {0}".format(_version)
        self.pixel = PixDrawing()
        self.qpixmap_image = None
        self.qpixmap_pixel = None
        self.settings_dict = {'shape': 'squares',
                              'available_shapes': ('circles', 'squares',
                                                   'filled squares'),
                              'pixels': [30, 30]}

        self.inImage_name = 'data/start_background.png'
        self.ui()
        self.load_file()
        self.dirty = False

    def ui(self):
        menubar = QMenuBar()
        menubar.setNativeMenuBar(True)  # make the menu bar OS specific

        bar_file = menubar.addMenu("&File")
        file_load = QAction("&Load image", self)
        file_load.setShortcut("Ctrl+N")

        file_save = QAction("&Save plate", self)
        file_save.setShortcut("Ctrl+S")

        file_print = QAction("&Print", self)
        file_print.setShortcut("Ctrl+P")

        file_settings = QAction("S&ettings", self)

        file_quit = QAction("&Quit", self)
        file_quit.setShortcut("Ctrl+Q")

        bar_file.addAction(file_load)
        bar_file.addAction(file_save)
        bar_file.addAction(file_print)
        bar_file.addAction(file_settings)
        bar_file.addAction(file_quit)

        bar_about = menubar.addMenu("&About")
        about_about = QAction("&About", self)
        about_licence = QAction("&Licence", self)
        about_QT = QAction("About &QT", self)
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

        file_load.triggered.connect(self.open_file)
        file_save.triggered.connect(self.save_file)
        file_print.triggered.connect(self.print_file)
        file_settings.triggered.connect(self.change_settings)
        file_quit.triggered.connect(self.close)

        about_about.triggered.connect(self.show_about)
        about_licence.triggered.connect(self.show_license)
        about_QT.triggered.connect(qApp.aboutQt)

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
        name = QFileDialog.getOpenFileNames(self, "Open Images",
                                                    os.path.expanduser("~"),
                                                    "Images (*.png *.jpg *.bmp"
                                                    " *.tif);;All Files (*)")
        self.inImage_name = name[0][0]
        self.load_file()

    def load_file(self):
        self.pixel.start_image = Image.open(self.inImage_name)
        self.qpixmap_image = QPixmap(self.inImage_name)
        self.label_image.setPixmap(self.qpixmap_image)
        self.refresh_plate()
        self.window_title = "PyBigPixel Creator {0} -- Untitled pattern".format(_version)
        self.setWindowTitle(self.window_title)
        self.dirty = True
        self.updatescreensize()

    def save_file(self):
        if self.inImage_name:
            saveFileName = QFileDialog.getSaveFileName(self, "PyBigPixel Creator {0}"
                                                       " -- Save Images"
                                                       .format(_version), '',
                                                       ".bmp")
            if saveFileName[0][-4:] == ".bmp":
                file = saveFileName[0]
            else:
                file = saveFileName[0] + saveFileName[1]

            self.pixel.pix_img.save(file)
            self.dirty = False
            self.window_title = "PyBigPixel Creator {0} -- {1}".format(_version, file[:-4].split('/')[-1])
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
                                                       .format(_version),
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
        about = AbouteInfo('data/about.html', 'About')
        about.exec_()

    def show_license(self):
        licence = AbouteInfo('data/gpl.html', 'License')
        licence.exec_()

    def refresh_plate(self):
        self.dirty = True
        if ('Untitled' not in self.window_title
            and '*' not in self.window_title):
            self.window_title = self.window_title + '*'
            self.setWindowTitle(self.window_title)

        if self.inImage_name:
            self.pixel.load_image(self.inImage_name)
            self.pixel.shape = self.settings_dict['shape']
            self.pixel.pixels_tot = self.settings_dict['pixels']
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
        self.setWindowTitle("PyBigPixel Creator {0}-- {1}".format(_version, name))
        self.cancelbutton.clicked.connect(self.close)


class Settings(QDialog):
    changed = pyqtSignal()

    def __init__(self, shape, parent=None):
        super(Settings, self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)
        # Make reference copy of variables
        self.shape = shape
        self.setWindowTitle("PyBigPixel Creator {0}-- {1}"
                            .format(_version, 'Settings'))

        shape_label = QLabel("Shape of pixel")
        self.shape_list = QComboBox()
        self.shape_list.addItems(self.shape['available_shapes'])
        self.shape_list.setCurrentIndex(self.shape_list.findText(self.shape['shape']))
        plate_label = QLabel("Number of PyBigPixel Creators"
                             "used (width x height)")
        plate_label_x = QLabel(" X ")
        self.pixel_button_width = QSpinBox()
        self.pixel_button_width.setRange(1, 250)
        self.pixel_button_width.setValue(self.shape['pixels'][0])

        self.pixel_button_height = QSpinBox()
        self.pixel_button_height.setRange(1, 250)
        self.pixel_button_height.setValue(self.shape['pixels'][1])

        layout = QGridLayout()
        layout.addWidget(shape_label, 0, 0)
        layout.addWidget(self.shape_list, 0, 1)
        layout.addWidget(plate_label, 1, 0)
        layout.addWidget(self.pixel_button_width, 1, 1)
        layout.addWidget(plate_label_x, 1, 2)
        layout.addWidget(self.pixel_button_height, 1, 3)

        button_layout = QVBoxLayout()
        buttonbox = QDialogButtonBox(QDialogButtonBox.Apply |
                                     QDialogButtonBox.Cancel)
        button_layout.addStretch()
        button_layout.addWidget(buttonbox)
        layout.addLayout(button_layout, 2, 0, 2, 4)
        self.setLayout(layout)

        buttonbox.rejected.connect(self.close)
        buttonbox.button(QDialogButtonBox.Apply).clicked.connect(self.apply)

    def apply(self):
        self.shape['pixels'][0] = self.pixel_button_width.value()
        self.shape['pixels'][1] = self.pixel_button_height.value()
        self.shape['shape'] = self.shape_list.currentText()
        self.changed.emit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
