#!/usr/bin/env python3

from PIL import Image, ImageChops

import argparse
import glob
import binascii
import os
import hashlib
import time
import random
import os

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

parser.add_argument("--alpha", help="Custom blend alpha multiplier", type=float, 
                  default=3)

args = parser.parse_args()


print("Blending all files in the following folders:")
print(", ".join(args.DIRS))

if args.R:
	print("And all sub-directories")

print("With extensions:")
print(", ".join(args.ext))


print("And sending them to file {}\n\n".format(args.o))

def match(path):
	return path.split(".")[-1] in args.ext

bands = []
img = None
mode = None
size = None

def sortDirectory(path):
  global bands, img, mode, size
  files = glob.glob("{}/*".format(path))
  for i in files:
    if os.path.isdir(i) and args.R and os.path.basename(i)!=args.o:
      sortDirectory(i)
    else:
      if match(i):
        bands.append(i)

for i in args.DIRS:
	sortDirectory(i)

print("Discovered {} images".format(len(bands)))

alpha =  (1.0 / len(bands)) * args.alpha
print("Using Alpha = {}".format(alpha))

print("(That's with multiplier {})".format(args.alpha))

for i in bands:
  j = Image.open(i)
  if not img:
    img = True
    mode = j.mode
    size = j.size
    img = Image.open(i)
    print("\nUSING SETTINGS")
    print("IMAGE MODE: {}".format(mode))
    print("IMAGE SIZE: X {}, Y {}\n".format(*size))
  else:
    j = Image.open(i)
    j = j.resize(size)
    j = j.convert(mode)
    img = ImageChops.blend(img, j, alpha)


img.save(args.o)

imgviewer = os.environ["IMAGEVIEWER"]

if imgviewer:
  print("Opening in {}".format(imgviewer))
  os.system("{} {}".format(imgviewer, args.o))
else:
  print("No imageviewer set -- Export to $IMAGEVIEWER")
