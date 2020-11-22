"""
Separate tiff stack into individual tiff files.
"""


import numpy as np
import tifffile as tif


def dissemble(tif_file, output_dir):

	stack = tif.imread(tif_file)

	n = stack.shape[0]
	for i in range(n):
		tile = stack[i,:,:]
		tif.imwrite(output_dir+"/s{}.tif".format(i), np.flip(tile, axis=0))
	