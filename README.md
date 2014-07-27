#PyBigPixel Creator
---
With PyBigPixel Creator software you can easily make big pixel art from you digital images. This images could also be use for:

* Tile art designs
* Cross stitch designs
* Quilt patches designs
* Bead plate templates for making advanced bead plates

![Screen shoot](https://github.com/SWE-JSAM/PyBigPixel-creator/blob/master/raw_files/PyBigPixel_screenshoot.png)

## Run the program
Check dependencies, see below, prior executing the program.

* Execute the file pearlplate.py
* Load a image, [see supported images](http://pillow.readthedocs.org/en/latest/handbook/image-file-formats.html),menu --> load image. The pearl plate template is generated.
* Print the pearl plate template or save it as a bmp file, menu -> Save/Print

## Settings menu
In the settings menu you can change some default settings.

* How many pixels should be used (default 30 x 30)
* The pixel it self:
    * 'circles': circular pixels
    * 'squares': squarer pixels with some space between them (default)
    * 'filled squares' without any space between pixels
    * 'cross': crosses that could be used for cross stitches
     
## Dependency's
* Python 3.x, currently the program also work with Python 2.7 branch
* pillow (have tested 2.5.0) [pillow home page](http://pillow.readthedocs.org/en/latest/)
* PyQt5 (have tested 5.3.1) [PyQt5 home page](http://pyqt.sourceforge.net/Docs/PyQt5/index.html)
* Have only tested on Linux. Please report issues if you are running outer platforms.

## Planed features

* Improve code: This is my first pyqt project.
* Add support for different pixel layouts: hexagons, rectangles and crosses for cross stitches
* Add Swedish languish support
* Make a setup script
* make resources files 
