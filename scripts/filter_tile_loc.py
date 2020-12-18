"""
Filter tile location file to include only valid tiles.
"""


import numpy as np
import os

import argparse

parser = argparse.ArgumentParser()

# IO
parser.add_argument("dir")

args = parser.parse_args()


def get_dir(file_path):

	m = ""
	i = 0
	while m != "/":

		i += 1
		m = file_path[-i]
		
	return file_path[:-i+1]


if __name__ == "__main__":

	d = args.dir
	
	fin = open(os.path.join(d, "tile_location.txt"), "r")
	fout = open(os.path.join(d, "tile_location_valid.txt"), "w")

	flist = os.listdir(os.path.join(d, "clahe"))
	flist = np.array(flist)

	for l in fin.readlines():

		elem = l[:-1].split(" ")
		if np.any(np.isin(flist, elem[0])):
			fout.write("{} {} {} {}\n".format(elem[0], elem[1], elem[2], elem[3]))

	fin.close()
	fout.close()
