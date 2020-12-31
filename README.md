# TileMaker
Python script to create tiled images from input images. This script takes all images in the directory it is run from and creates tiled output images in a new /tiles subdirectory from them.
The output images contain n x n input images, cropped to the deisred aspect ratio. The crop is centered, retaining as much of the original image as possible.

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

## Basic usage
The default settings are for the usecase of compiling images onto 2x2 tiles with 6:4 aspect ratio of a reasonable resolution to print at a photo kiosk for subsequent cutting. Simply, from within the directory that contains your phoots, run 

```console
$ python3 <path to TileMaker>/TileMaker.py
```
and it will create a subidrectory /tiles filled with output images like this:

<img src="https://user-images.githubusercontent.com/8363989/103384010-18e47380-4af5-11eb-98db-43cd2c597e91.jpg" width="500">
(Images sourced from https://unsplash.com/s/photos/vacation)

## Advanced usage
But this little script can do a lot more. For example you can turn rotation off, set the aspect ratio to 1:1, crank up the resolution and compile your 16 favorite holiday pictures onto a square format for a printed poster gift. The command for this would be something like

```console
$ TileMaker.py -a 1 1 -o -n 4 -res 10000
```
and will produce something like this:

<img src="https://user-images.githubusercontent.com/8363989/103385355-48e24580-4afa-11eb-9451-50c890e07d3f.jpg" width="500">
(Images sourced from https://unsplash.com/s/photos/vacation)


# Requirements
TileMaker relies on OpenCV and Numpy. If you don't have them installed yet you can install them by running
```console
pip3 install -r requirements.txt
```
If this fails, make sure your pip is up to date with
```console
pip3 install --upgrade pip
```
