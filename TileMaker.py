#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import os
import time
import argparse
import sys

# crop centered to a given aspect ratio, keeping as much as possible
def max_crop_aspect_ratio(img, rel_height, rel_width):
    img_aspect_ratio = float(img.shape[0]) / img.shape[1]
    aspect_ratio = float(rel_height) / rel_width

    if img_aspect_ratio > aspect_ratio:
        # image is too high
        new_height = img.shape[1] * aspect_ratio
        crop_start = img.shape[0] / 2 - new_height / 2
        return img[int(crop_start) : int(crop_start + new_height), :]
    elif img_aspect_ratio < aspect_ratio:
        # image is too wide
        new_width = img.shape[0] / aspect_ratio
        crop_start = img.shape[1] / 2 - new_width / 2
        return img[:, int(crop_start) : int(crop_start + new_width)]
    else:
        # image is already perfect
        return img


# resize with given height resolution and aspect ratio
def resize(img, height_pixels, rel_height, rel_width):
    width_pixels = height_pixels * float(rel_width) / rel_height
    return cv2.resize(img, (int(width_pixels), height_pixels))


# Write image buffer to file with a useful name
def flushToFile(img_, path_, tile_size_, image_counter_):
    output_filename = "{}x{}_tile_{}.jpg".format(
        tile_size_, tile_size_, str(image_counter_).zfill(3)
    )
    # make output dir if this is the fist image to create
    if not os.path.exists(path_):
        os.makedirs(path_)
        time.sleep(0.1)  # os.makedirs() takes a while
    cv2.imwrite(path_ + output_filename, img_)


def main():
    parser = argparse.ArgumentParser(
        description="""Creates images with n x n tiles from images in 
        the directory this script is run from. Saves the crated images 
        in a new directory /tiles."""
    )
    parser.add_argument(
        "-n",
        metavar="tileNum",
        type=int,
        default=2,
        help="The n in n x n tiles. Default is 2.",
    )
    parser.add_argument(
        "-aspect",
        metavar=("Height", "Width"),
        nargs=2,
        type=int,
        default=(6, 4),
        help="Tupel of numerator and denominator. Default is 6:4.",
    )
    parser.add_argument(
        "-res",
        metavar="outputRes",
        type=int,
        default=2400,
        help="Pixels in long side of output images. Default is 2400.",
    )
    parser.add_argument(
        "-o",
        default=True,
        action="store_false",
        help="Switch off automatic input image rotation.",
    )

    # parse command line arguments
    args = parser.parse_args()
    tile_size = args.n
    aspect_height = args.aspect[0]
    aspect_width = args.aspect[1]
    height_pixels = args.res
    align = args.o
    
    # fixed parameters
    source_directory = os.getcwd()
    output_directory = "tiles/"

    aspect_ratio = float(aspect_height) / aspect_width
    if aspect_ratio < 1:
        print("Aspect ratio must not be smaller than 1! Exiting.")
        sys.exit()
    width_pixels = int(height_pixels / aspect_ratio)

    # create buffer and make white
    tile_buffer = np.zeros((height_pixels, width_pixels, 3), np.uint8)
    tile_buffer[:, :] = (255, 255, 255)
    tile_counter = 0
    image_counter = 0
    input_counter = 0

    for filename in os.listdir(source_directory):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            input_counter = input_counter + 1
            fullpath = os.path.join(source_directory, filename)
            print("\nProcessing " + fullpath)

            # load image
            img = cv2.imread(fullpath)

            if align:
                # rotate if necessary
                if img.shape[0] < img.shape[1]:
                    print("Rotating image to portrait mode")
                    img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)

            # crop to desired aspect ratio
            print(
                "Cropping image to aspect ratio {} x {}".format(
                    aspect_height, aspect_width
                )
            )
            img = max_crop_aspect_ratio(img, aspect_height, aspect_width)

            # resize
            print("Resizing image to {} pixels".format(int(height_pixels / tile_size)))
            img = resize(
                img, int(height_pixels / tile_size), aspect_height, aspect_width
            )

            # paste processed image into buffer
            row_index = int(tile_counter / tile_size)
            collumn_index = tile_counter % tile_size
            height_start = int(row_index * height_pixels / tile_size)
            height_end = int(height_start + height_pixels / tile_size)
            width_start = int(collumn_index * width_pixels / tile_size)
            width_end = int(width_start + width_pixels / tile_size)

            tile_buffer[height_start:height_end, width_start:width_end] = img

            # increment or reset tile counter
            tile_counter = (tile_counter + 1) % tile_size ** 2

            # write full image to file
            if tile_counter == 0:
                flushToFile(tile_buffer, output_directory, tile_size, image_counter)
                image_counter = image_counter + 1
                # clear buffer
                tile_buffer[:, :] = (255, 255, 255)
        else:
            # skip non-image files
            continue

    # write the incomplete tile pattern, if any
    if tile_counter != 0:
        flushToFile(tile_buffer, output_directory, tile_size, image_counter)
        image_counter = image_counter + 1

    print("\nCreated {} tiles out of {} images".format(image_counter, input_counter))


if __name__ == "__main__":
    main()
