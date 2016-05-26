#!/usr/bin/env python3

from PIL import Image

import argparse
import glob
import binascii
import os
import hashlib
import time
import random

r = random.Random()
default_filename = time.strftime("blend-%H%M%S_{}.png".format(r.randint(1,100)))

parser = argparse.ArgumentParser(description='Blend Images')

parser.add_argument('-o', metavar="[Filename]", help='The output file', default=default_filename)

parser.add_argument('DIRS', help="The input directories",
		    metavar="DIR", nargs="+")

parser.add_argument('--ext', metavar='Ext', help='The extensions to use',
		    default=["jpg", "png", "jpeg"], nargs="*")

parser.add_argument("-R", action="store_true", default=False,
			help="Recursively look through the input directories")


args = parser.parse_args()


print("Blending all files in the following folders:")
print(", ".join(args.DIRS))

if args.R:
	print("And all sub-directories")

print("With extensions:")
print(", ".join(args.ext))


print("And sending them to file {}/\n\n".format(args.o))

def match(path):
	return path.split(".")[-1] in args.ext


img = None

def sortDirectory(path):
  global img
  files = glob.glob("{}/*".format(path))
  for i in files:
    if os.path.isdir(i) and args.R and os.path.basename(i)!=args.o:
      print("DIRECTORY {}".format(i))
      sortDirectory(i)
    else:
      if match(i):
        if not img:
          img = Image.open(i)
        else:
          j = Image.open(i)
          if j.size != img.size:
            j = j.resize(img.size)
          if j.mode != img.mode:
            j = j.convert(img.mode)
          img = Image.blend(img,j, 0.5)


for i in args.DIRS:
	sortDirectory(i)

img.save(args.o)
