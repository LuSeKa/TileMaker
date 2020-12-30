#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import os
import time

## expected inputs:
# source directory
# target directory (create if it does not exist)
# aspect ratio (height and width)
# image height (longer dimension) in pixels

source_directory = os.getcwd()
target_directory = 'tiles/'
aspect_height = 6 #  height must be greater than width
aspect_width = 4
height_pixels = 2048
tile_size = 2
image_flash_time = 1

if aspect_height < aspect_width:
    quit

master_aspect_ratio = float(aspect_height)/aspect_width
width_pixels = int(height_pixels / master_aspect_ratio)


# create buffer and make white
tile_buffer = np.zeros((height_pixels, width_pixels, 3), np.uint8)
tile_buffer[:,:] = (255, 255, 255)
#cv2.imshow("buffer", tile_buffer)
 

def max_crop_aspect_ratio(img, rel_height, rel_width):
    img_aspect_ratio = float(img.shape[0])/img.shape[1]
    # print(master_aspect_ratio)
    # print(img_aspect_ratio)
    aspect_ratio = float(rel_height)/rel_width
        
    if img_aspect_ratio > aspect_ratio:
        # image is too high
        new_height = img.shape[1] * aspect_ratio
        crop_start = img.shape[0]/2 - new_height/2
        return img[int(crop_start):int(crop_start + new_height), :]
    elif img_aspect_ratio < aspect_ratio:
        # image is too wide
        new_width = img.shape[0] / aspect_ratio
        crop_start = img.shape[1]/2 - new_width/2
        return img[:, int(crop_start):int(crop_start + new_width)]
        return img
    else:
        # image is already perfect
        return img    
 
def resize(img, height_pixels, rel_height, rel_width):
    width_pixels = float(height_pixels) * float(rel_width)/rel_height
    # print(int(height_pixels))
    # print(int(width_pixels))
    return cv2.resize(img, (int(width_pixels), int(height_pixels)))


tile_counter = 0
image_counter = 0
for filename in os.listdir(source_directory):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        fullpath = os.path.join(source_directory, filename)
        print("Processing " + fullpath)
        
        # load image
        img = cv2.imread(fullpath)
        
        # rotate if necessary
        print(img.shape)
        if img.shape[0] < img.shape[1]:
            print("Image is in wrong orienation. Rotating...")
            img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)            
        
        # crop to desired aspect ratio
        print("Cropping image to desired aspect ratio")
        img = max_crop_aspect_ratio(img, aspect_height, aspect_width)
        
        # resize
        print("Resizing to desired resolution")
        img = resize(img, height_pixels/tile_size, aspect_height, aspect_width)
        print(img.shape)
        
        # cv2.imshow("Processed image", img)  
        # cv2.waitKey(0)
        
        # paste processed image into buffer
        row_index = tile_counter / tile_size
        collumn_index = tile_counter % tile_size
        # print(row_index)
        # print(collumn_index)
        height_start = int(row_index * height_pixels/tile_size)
        height_end = int(height_start + height_pixels/tile_size)
        width_start = int(collumn_index * width_pixels/tile_size)
        width_end = int(width_start + width_pixels/tile_size)
        
        tile_buffer[height_start:height_end, width_start:width_end] = img
        
        # increment or reset tile counter
        tile_counter = (tile_counter + 1) % 4
        
        # write full image to file
        if tile_counter == 0:        
            tile_counter = 0
            output_filename = str(tile_size) + "x" + str(tile_size) + "_tile_" + str(image_counter).zfill(3) + ".jpg"
            if image_counter == 0:
           # make output path if this is the fist image to create
                if not os.path.exists(target_directory):
                    os.makedirs(target_directory)
                    time.sleep(0.1) 
            cv2.imwrite(target_directory + output_filename,tile_buffer)
            image_counter = image_counter + 1
            cv2.imshow(output_filename, tile_buffer)
            cv2.waitKey(image_flash_time)
            cv2.destroyAllWindows()
            # clear tile buffer
            tile_buffer[:,:] = (255, 255, 255)
    else:
        continue
        
# write the remainder to file, if any
if tile_counter != 0:
    output_filename = str(tile_size) + "x" + str(tile_size) + "_tile_" + str(image_counter + 1).zfill(3) + ".jpg"
    # make output path if this is the fist image to create
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)
        time.sleep(0.1) 
    cv2.imwrite(target_directory + output_filename,tile_buffer)   
    image_counter = image_counter + 1 
    cv2.imshow(output_filename, tile_buffer)
    cv2.waitKey(image_flash_time)
    cv2.destroyAllWindows()

print("Created " + str(image_counter) + " tiles!")
quit()
    

