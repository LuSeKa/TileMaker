#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import os

## expected inputs:
# source directory
# target directory (create if it does not exist)
# aspect ratio (height and width)

source_directory = 'raw/'
target_directory = 'tiles/'
aspect_height = 6 #  height must be greater than width
aspect_width = 4

height_pixels = 1024

if aspect_height < aspect_width:
    quit

master_aspect_ratio = float(aspect_height)/aspect_width

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
    width_pixels = float(height_pixels) * float(rel_height)/rel_width
    print(int(height_pixels))
    print(int(width_pixels))
    return cv2.resize(img, (int(height_pixels), int(width_pixels)))

for filename in os.listdir(source_directory):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        fullpath = os.path.join(source_directory, filename)
        print("Processing " + fullpath)
        
        # load image
        img = cv2.imread(fullpath)
        
        # rotate if necessary
        if float(img.shape[0])/img.shape[1] < master_aspect_ratio:
            print("Image is in wrong orienation. Rotating...")
            img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)            
        
        # crop to desired aspect ratio
        print("Cropping image to desired aspect ratio")
        img = max_crop_aspect_ratio(img, aspect_height, aspect_width)
        
        # resize
        print("Resizing to desired resolution")
        img = resize(img, height_pixels, aspect_height, aspect_width)
        
        cv2.imshow("Processed image", img)  
        cv2.waitKey(0)
        
    else:
        continue




