"""
Extract tile locations and generate tile_location.txt file.
"""


import argparse

parser = argparse.ArgumentParser()

# IO
parser.add_argument("st_file")
parser.add_argument("--offset", type=int)
parser.add_argument("--prefix", required=False, default="")


args = parser.parse_args()


def generate_tile_loc(st_file, out_file, offset=0, prefix=""):

	f_in = open(st_file, "rb")
	f_in.read(1024) # Read HEADER

	f_out = open(out_file, "w")

	v = 1
	i = 0

	tile_bin = f_in.read(12)
	while v != 0:

		xloc = int.from_bytes(tile_bin[2:4], "little")
		yloc = int.from_bytes(tile_bin[4:6], "little")
		zloc = int.from_bytes(tile_bin[6:8], "little")

		f_out.write(prefix+"s{0:04d}.tif {1} {2} {3}\n".format(i, xloc, yloc, zloc+offset))

		tile_bin = f_in.read(12)
		v = int.from_bytes(tile_bin, "little")
		
		i += 1

	f_in.close()
	f_out.close()


def get_dir(file_path):

	m = ""
	i = 0
	while m != "/":

		i += 1
		m = file_path[-i]
		

	return file_path[:-i+1]


if __name__ == "__main__":

	img_file = args.st_file
	prefix = args.prefix
	offset = args.offset

	img_dir = get_dir(img_file)

	output_file = "/home/jabae/tile_location_new.txt"
	generate_tile_loc(img_file, output_file, offset, prefix)
