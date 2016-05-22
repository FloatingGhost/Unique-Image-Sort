#!/usr/sbin/python3

from PIL import Image

import argparse
import glob
import binascii
import os
import hashlib

parser = argparse.ArgumentParser(description='Sort Images')

parser.add_argument('-o', metavar="DIR", help='The output directory', default="unique")
parser.add_argument('DIRS', help="The input directories",
		    metavar="DIR", nargs="+")

parser.add_argument('--ext', metavar='Ext', help='The extensions to use',
		    default=["jpg", "png", "jpeg"], nargs="*")

parser.add_argument("-R", action="store_true", default=False,
			help="Recursively look through the input directories")

parser.add_argument("-X", action="store_true", default=False,
		   help="Execute the sort")

parser.add_argument("--clean", action="store_true", default=False,
			help="Clean the output folder (if it exists)")

parser.add_argument("--rename", action="store_true", default=False,
			help="Rename the images")
parser.add_argument("--sfw", action="store_true", default=False,
                        help="Discard possible lewd images")

args = parser.parse_args()


if not args.X:
	print("----DRY RUN----")
print("Sorting all files in the following folders:")
print(", ".join(args.DIRS))

if args.R:
	print("And all sub-directories")

print("With extensions:")
print(", ".join(args.ext))


print("And sending them to directory {}/\n\n".format(args.o))

s = set()

if not os.path.exists(args.o):
	print("mkdir {}".format(args.o))
	if args.X:
		os.mkdir(args.o)
else:
	if args.clean:
		print("rm -rf {}/*".format(args.o))
		if args.X:
			os.system("rm -rf {}/*".format(args.o))

def match(path):
	return path.split(".")[-1] in args.ext

picno = 0
def rename(fname):
	global picno
	if not args.rename:
		return fname
	else:
		p = str(picno)
		r = "0"*(5-len(p))
		r += p
		r += "." + fname.split(".")[-1]
		picno += 1	
		return r

def lewd(j):
	dat = list(j.getdata())
	lewdness = [x for x in dat if x[0] == 255 and x[1] == 245 and x[2]>215]
	l = len(dat)
	print("Lewdness {}".format((len(lewdness)/l)*100))

def sortDirectory(path):
	files = glob.glob("{}/*".format(path))
	
	for i in files:
		if os.path.isdir(i) and args.R and os.path.basename(i)!=args.o:
			print("DIRECTORY {}".format(i))
			sortDirectory(i)
		else:
			if match(i):
				j = Image.open(i)
				lewd(j)
				data = (binascii.hexlify(j.tobytes()))
				h = hashlib.md5(data)
				d = h.hexdigest()
				if d not in s:
					s.add(d)
					#File is ok!
					cmd = ("cp '{}' '{}/{}'".format(i, args.o, 
							rename(os.path.basename(i))))
					print(cmd)
					if args.X:
						os.system(cmd)
					


for i in args.DIRS:
	sortDirectory(i)

if not args.X:
	print("\n\nAdd -X to your arguments if this looks ok!")
