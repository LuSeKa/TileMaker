# TileMaker
Python script to create tiled images from input images. This script takes all images in the directory it is run from and creates tiled output images in a new /tiles subdirectory from them.
The output images contain n x x input images, cropped to the deisred aspect ratio. The crop is centered, retaining as much of the original image as possible.

It accepts several command line arguments to customize the output. Call with argument -h to see the this help:

```console
usage: TileMaker.py [-h] [-n tileNum] [-aspect Height Width] [-res outputRes]
                    [-o]

Creates images with n x n tiles from images in the directory this script is
run from. Saves the crated images in a new directory /tiles.

optional arguments:
  -h, --help            show this help message and exit
  -n tileNum            The n in n x n tiles. Default is 2.
  -aspect Height Width  Tupel of numerator and denominator. Default is 6:4.
  -res outputRes        Pixels in long side of output images. Default is 2400.
  -o                    Switch off automatic input image rotation.
```
The default settings are for the usecase of compiling images onto 2x2 tiles with 6:4 aspect ratio of a reasonable resolution to print at a photo kiosk (e.g. CVS) for subsequent cutting and scrapbooking (the default printable images are just too large for scrapbooks imho).

But this little script can do a lot more. For example you can turn rotation off, set the aspect ratio to 1:1, crank up the resolution and compile your 100 favorite holiday pictures onto a square format for a great printed poster gift. The command for this would be something like

```console
TileMaker.py -a 1 1 -o -n 10 -res 10000
```

# Requirements
TileMaker relies on OpenCV and Numpy. If you don't have them installed yet you can install them by running
```console
pip3 install -r requirements.txt
```
If this fails, make sure your pip is up to date with
```console
pip3 install --upgrade pip
```
