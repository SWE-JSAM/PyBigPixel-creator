#PyBigPixel Creator
---
With PyBigPixel Creator software you can easily make big pixel art from you digital images. This images could also be use for:

* Tile art designs
* Cross stitch designs
* Quilt patches designs (hexagons coming soon)
* Bead plate templates for making bead plates

See **settings menu**, below, for supported pixels.

![Screen shoot](https://github.com/SWE-JSAM/PyBigPixel-creator/blob/master/raw_files/PyBigPixel_screenshoot.png)

## Run the program
Check dependencies, see below, prior executing the program. To run the program just install it using the setup.py file:

    $ sudo python setup.py install
After the installation you can start the program in the terminal by typing:

    $ pybigpixel

Alternatively you can start the program using the run.py script.

Uninstall the program using pip:

    $ sudo pip uninstall pybigpixel-creator

## Using PyBigPixel Creator
* Load a image, [see supported images](http://pillow.readthedocs.org/en/latest/handbook/image-file-formats.html),menu --> load image. The pearl plate template is generated.
* Print the pearl plate template or save it as a bmp file, menu -> Save/Print

## Settings menu
In the settings menu you can change some default settings.

* The pixel it self:
    * 'circles': circular pixels
    * 'squares': squarer pixels with some space between them (default)
    * 'filled squares' without any space between pixels
    * 'cross': crosses that could be used for cross stitches
* Background color: The background color could be selected from several different available backgrounds (default gray)
* How many pixels should be used (default 30 x 30)     

## Dependency's
* Python 3.x, currently the program also work with Python 2.7 branch
* pillow (have tested 2.5.0) [pillow home page](http://pillow.readthedocs.org/en/latest/)
* PyQt5 (have tested 5.3.1) [PyQt5 home page](http://pyqt.sourceforge.net/Docs/PyQt5/index.html)
* Have only tested on Linux. Please report issues if you are running outer platforms.



## Planed features

* Improve code base: This is my first PyQt5 project. If you have any suggestions about code improvement just contact me. 
* Add support for additional pixel layouts: hexagons and rectangles
* make resources files
* Make some illustrations for the software
* Linux packages for Arch Linux is planned

## Change log
### Version 0.2.0
* Add translation in code
    *Added Swedish languish support
 
#### Version 0.1.5

* Added setup script for simpler installation/uninstall.
 