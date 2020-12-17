"""
Apply clahe on tiles in the folder.
"""


import numpy as np
import tifffile as tif
import os

import cv2

import argparse

parser = argparse.ArgumentParser()

# IO
parser.add_argument("tif_folder")

args = parser.parse_args()


def read_tif(fname):
    
    t = tif.imread(fname)
    img = np.zeros(t.shape)
    img[:,:] = tif.imread(fname)
    
    return img


def normalize(tile):
    
    vmin = tile.min(); vmax = tile.max()
    new_tile = (tile-vmin)*255/(vmax-vmin)
    
    return new_tile.astype("uint8")


def get_dir(file_path):

	m = ""
	i = 0
	while m != "/":

		i += 1
		m = file_path[-i]
		
	return file_path[:-i+1]


if __name__ == "__main__":

	img_dir = args.tif_folder
	
	prev_dir = get_dir(img_dir)
	out_dir = os.path.join(prev_dir,"clahe/")

	if not os.path.isdir(out_dir):
		os.makedirs(out_dir)

	clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))

	flist = os.listdir(img_dir)
	for i in range(len(flist)):

		fname = os.path.join(img_dir, flist[i])
		img = read_tif(fname)
		img = normalize(img)


		if np.var(img)>30:

			tif.imwrite(os.path.join(out_dir, flist[i]), clahe.apply(img))

