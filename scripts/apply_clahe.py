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
parser.add_argument("dir")

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

	data_dir = args.dir
	img_dir = os.path.join(data_dir, "tif/")
	
	out_dir = os.path.join(data_dir,"clahe_new/")

	if not os.path.isdir(out_dir):
		os.makedirs(out_dir)

	clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))

	# Count number of tiles
	f = open(os.path.join(data_dir, "tile_location.txt"), "r")
	
	img_list = []; x_list = []; y_list = []; z_list =[]
	for l in f.readlines():
		elem = l[:-1].split(" ")
		img_list.append(elem[0])
		x_list.append(int(elem[1]))
		y_list.append(int(elem[2]))
		z_list.append(int(elem[3]))

	f.close()

	img_list = np.array(img_list)
	coord_list = np.zeros((len(x_list),3))
	coord_list[:,0] = x_list; coord_list[:,1] = y_list; coord_list[:,2] = z_list

	layers = np.unique(coord_list[:,2])
	for z in layers:

		valid = coord_list[:,2]==z
		
		img_layer = img_list[valid]
		x_layer = coord_list[valid,0]
		y_layer = coord_list[valid,1]
		
		x_uniq = np.unique(x_layer)
		y_uniq = np.unique(y_layer)
		var_arr = np.zeros((x_uniq.shape[0], y_uniq.shape[0]))
		img_arr = np.ones((x_uniq.shape[0], y_uniq.shape[0]))*-1

		for i in range(img_layer.shape[0]):

			fname = os.path.join(img_dir, img_layer[i])
			img = read_tif(fname)
			img = normalize(img)
			img = clahe.apply(img)
			
			br = 95
			if np.mean(img)<50:
				a = (200/np.var(img))**0.5
				img = np.clip((img-np.mean(img))*a + br, 0, 255)

			else:
				img = np.clip((img + (br-np.mean(img))), 0, 255)

			tif.imwrite(os.path.join(out_dir, img_layer[i]), img.astype("uint8"))
