"""
Export transformed sections.
"""


import numpy as np
import pandas as pd
import tifffile as tif
import os
import itertools

from scipy import ndimage

import argparse

parser = argparse.ArgumentParser()

# IO
parser.add_argument("dir")
parser.add_argument("--size", nargs="+", type=int, required=True)

args = parser.parse_args()



def distance(p1, p2):

	return np.sum((p1 - p2)**2, axis=1)**0.5


# def compute_penalty(img):

# 	x_size = img.shape[0]
# 	y_size = img.shape[1]
# 	x_range = np.arange(x_size)
# 	y_range = np.arange(y_size)
# 	coords = np.array(list(itertools.product(x_range, y_range)))

# 	center = np.array([np.median(coords[:,0]), np.median(coords[:,1])])
# 	center = center.reshape((1,2))

# 	p = np.sum((coords - center)**2, axis=1)**0.5

# 	return p.reshape((x_size, y_size))


def compute_penalty(img, x_off, y_off, w, h):

	ctr = np.array([int(x_off), int(y_off)]).reshape((1,2))

	d = np.min([distance(ctr, np.array([0,0])),
							distance(ctr, np.array([h,0])),
							distance(ctr, np.array([0,w])),
							distance(ctr, np.array([h,w]))])

	# d = 1 - d/((w/2**2+h/2**2)**0.5)/2
	p = np.ones(img.shape)*d

	return p


if __name__ == "__main__":

	data_dir = args.dir
	img_dir = os.path.join(data_dir, "transformed")
	out_dir = os.path.join(data_dir, "export_010520")
	# out_dir = "/data/research/se/celegans/dataset3/N2DA_1430-2/Merged/sections

	if not os.path.isdir(out_dir):
		os.makedirs(out_dir)

	f_trans = os.path.join(data_dir, "transform.csv")
	trans_df = pd.read_csv(f_trans, header=None)
	img_list = trans_df[0]
	n_img = img_list.shape[0]

	img_loc = []
	x_loc = []
	y_loc = []
	f_loc = open(os.path.join(data_dir, "tile_location.txt"), "r")
	for l in f_loc.readlines():

		elem = l.split(" ")
		img_loc.append(elem[0])
		x_loc.append(int(elem[1]))
		y_loc.append(int(elem[2]))

	img_loc = np.array(img_loc)
	x_loc = np.array(x_loc)
	y_loc = np.array(y_loc)

	f_loc.close()

	# X, Y offset
	x_off_list = np.array(trans_df[2])
	y_off_list = np.array(trans_df[3])

	if x_off_list.min() < 0:
		x_off_list = x_off_list - x_off_list.min()
	if y_off_list.min() < 0:
		y_off_list = y_off_list - y_off_list.min()

	# Z index
	z_list = np.unique(trans_df[1])

	size = args.size
	w = size[0]
	h = size[1]
	

	for z in z_list:

		valid = trans_df[1]==z
		img_layer = np.array(img_list[valid])
		n_img_layer = img_layer.shape[0]

		x_off_layer = x_off_list[valid]
		y_off_layer = y_off_list[valid]
		w_tile_layer = np.array(trans_df[4][valid])
		h_tile_layer = np.array(trans_df[5][valid])

		img_sect = np.zeros((h,w), dtype="uint8")
		wt_sect = np.zeros((h,w))
		img_sect = img_sect.reshape((-1,))
		wt_sect = wt_sect.reshape((-1,))

		for i in range(n_img_layer):

			fname = os.path.join(img_dir, img_layer[i])
			tile = tif.imread(fname)

			x_off = x_off_layer[i]
			y_off = y_off_layer[i]
			w_tile = w_tile_layer[i]
			h_tile = h_tile_layer[i]

			tile_idx = np.where(img_loc==img_layer[i])[0]
			wt_tile = compute_penalty(tile, y_loc[tile_idx], x_loc[tile_idx], w, h)
			wt_tile[np.where(tile==0)] = 0

			img_temp = np.zeros((h,w))
			wt_temp = np.zeros((h,w))

			# print(y_off+h_tile, x_off+w_tile)
			img_temp[y_off:y_off+h_tile,x_off:x_off+w_tile] = tile
			wt_temp[y_off:y_off+h_tile,x_off:x_off+w_tile] = wt_tile
			img_temp = img_temp.reshape((-1,))
			wt_temp = wt_temp.reshape((-1,))

			valid = wt_sect < wt_temp
			img_sect[valid] = img_temp[valid]
			wt_sect[valid] = wt_temp[valid]
			# print(i)

		img_sect = img_sect.reshape(h,w)

		fname_out = os.path.join(out_dir, "z_{}.tif".format(z)) 
		tif.imwrite(fname_out, img_sect)
		print("z = {} exported".format(z))
