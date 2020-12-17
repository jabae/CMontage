"""
Separate tiff stack into individual tiff files.
"""


import numpy as np
import tifffile as tif
import os

import argparse

parser = argparse.ArgumentParser()

# IO
parser.add_argument("tif_file")

args = parser.parse_args()


def dissemble(tif_file, output_dir, flip=True):

	stack = tif.imread(tif_file)

	n = stack.shape[0]
	for i in range(n):
		tile = stack[i,:,:]
		if flip:
			tif.imwrite(output_dir+"/s{0:04d}.tif".format(i), np.flip(tile, axis=0))
		else:
			tif.imwrite(output_dir+"/s{0:04d}.tif".format(i), tile)


def get_dir(file_path):

	m = ""
	i = 0
	while m != "/":

		i += 1
		m = file_path[-i]
		

	return file_path[:-i+1]


if __name__ == "__main__":

	img_file = args.tif_file
	
	img_dir = get_dir(img_file)
	img_dir = img_dir + "tif"

	if not os.path.isdir(img_dir):
		os.makedirs(img_dir)

dissemble(img_file, img_dir)
