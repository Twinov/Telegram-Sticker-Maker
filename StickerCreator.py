#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Takes an image and makes it compatible for a Telegram Sticker.

This script takes a cropped image and turns it into
the appropriate size for use in a Telegram Sticker
formatting it into a 512x512px png for Telegram

if the export filename end in .webp, the script will
instead export the image as a webp.
This is useful because webp images uploaded to Telegram
are automatically formatted as stickers
"""
__version__ = "1.2"
__author__ = "Marc Hoeltge"

import sys
import os
import random
import string
from wand.image import Image
from wand.display import display
from PIL import Image as pilimg

try:
    with Image(filename=sys.argv[1]) as img:
        IMAGE_SIDE_LENGTH_PX = 512

        webp_requested = False;

        if len(sys.argv) == 3:
            if sys.argv[2][-5:] == ".webp":
                webp_requested = True

        #create a random string
        rand_string = ''.join([random.choice(string.ascii_letters) for n in range(10)])

        #autocrop the image to get rid of transparent space outlining it
        img.trim()

        #determine if width is the longest side of the image
        width_longest_side = True
        if img.width < img.height:
            width_longest_side = False

        if width_longest_side:
            #find the ratio that the short side will have to be scaled
            scale_ratio = float(IMAGE_SIDE_LENGTH_PX) / img.width
            new_height = int(round(scale_ratio * img.height))

            #crop the image into the smallest size possible
            img.resize(IMAGE_SIDE_LENGTH_PX, new_height)

            #create a new blank image and make a composite with the cropped image
            with Image(width=IMAGE_SIDE_LENGTH_PX, height=IMAGE_SIDE_LENGTH_PX) as new_img:
                top = (IMAGE_SIDE_LENGTH_PX - new_height) / 2
                new_img.composite(img, left=0, top=top)

                if webp_requested:
                    new_img.format = "png"
                    new_img.save(filename = rand_string + ".png")
                    final_img = pilimg.open(rand_string + ".png")
                    try:
                        final_img.save("res/" + sys.argv[2])
                        os.remove(rand_string + ".png")
                    except IOError:
                        print("error in webp conversion")
                elif len(sys.argv) == 3:
                    new_img.format = "png"
                    if sys.argv[2][-4:] == ".png":
                        new_img.save(filename="res/" + sys.argv[2])
                    else:
                        new_img.save(filename="res/" + sys.argv[2] + ".png")
                else:
                    new_img.format = "png"
                    new_img.save(filename="res/output.png")

        #repeat the above code but in terms of the height being the longest side
        else:
            scale_ratio = float(IMAGE_SIDE_LENGTH_PX) / img.height
            new_width = int(round(scale_ratio * img.width))
            img.resize(new_width, IMAGE_SIDE_LENGTH_PX)
            with Image(width=IMAGE_SIDE_LENGTH_PX, height=IMAGE_SIDE_LENGTH_PX) as new_img:
                left = (IMAGE_SIDE_LENGTH_PX - new_width) / 2
                new_img.composite(img, left=left, top=0)

                if webp_requested:
                    new_img.format = "png"
                    new_img.save(filename = rand_string + ".png")
                    final_img = pilimg.open(rand_string + ".png")
                    try:
                        final_img.save("res/" + sys.argv[2])
                        os.remove(rand_string + ".png")
                    except IOError:
                        print("error in webp conversion")
                elif len(sys.argv) == 3:
                    new_img.format = "png"
                    if sys.argv[2][-4:] == ".png":
                        new_img.save(filename="res/" + sys.argv[2])
                    else:
                        new_img.save(filename="res/" + sys.argv[2] + ".png")
                else:
                    new_img.format = "png"
                    new_img.save(filename="res/output.png")
except IOError:
    print ("Not a valid file")
