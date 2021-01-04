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


def compute_penalty(img):

	x_size = img.shape[0]
	y_size = img.shape[1]
	x_range = np.arange(x_size)
	y_range = np.arange(y_size)
	coords = np.array(list(itertools.product(x_range, y_range)))

	center = np.array([np.median(coords[:,0]), np.median(coords[:,1])])
	center = center.reshape((1,2))

	p = np.sum((coords - center)**2, axis=1)**0.5

	return p.reshape((x_size, y_size))


if __name__ == "__main__":

	data_dir = args.dir
	img_dir = os.path.join(data_dir, "transformed")

	f_trans= os.path.join(data_dir, "transform.csv")
	trans_df = pd.read_csv(f_trans, header=None)
	img_list = trans_df[0]
	n_img = img_list.shape[0]

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

		img_sect = np.zeros((h,w), dtype="uint8")
		wt_sect = np.ones((h,w))*9999
		img_sect = img_sect.reshape((-1,))
		wt_sect = wt_sect.reshape((-1,))

		for i in range(n_img):

			fname = os.path.join(img_dir, img_list[i])
			tile = tif.imread(fname)

			wt_tile = compute_penalty(tile)
			wt_tile[np.where(tile==0)] = 9999

			x_off = x_off_list[i]
			y_off = y_off_list[i]
			w_tile = trans_df[4][i]
			h_tile = trans_df[5][i]

			img_temp = np.zeros((h,w))
			wt_temp = np.ones((h,w))*9999

			img_temp[y_off:y_off+h_tile,x_off:x_off+w_tile] = tile
			wt_temp[y_off:y_off+h_tile,x_off:x_off+w_tile] = wt_tile
			img_temp = img_temp.reshape((-1,))
			wt_temp = wt_temp.reshape((-1,))

			valid = wt_sect > wt_temp
			img_sect[valid] = img_temp[valid]
			wt_sect[valid] = wt_temp[valid]
			print(i)


		img_sect = img_sect.reshape(h,w)

		fname_out = os.path.join(data_dir, "z_{}.tif".format(z)) 
		tif.imwrite(fname_out, img_sect)
