"""
Extract tile locations and generate tile_location.txt file.
"""


def generate_tile_loc(st_file, out_file):

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

		f_out.write("s{}.tif {} {} {}\n".format(i, xloc, yloc, zloc))

		tile_bin = f_in.read(12)
		v = int.from_bytes(tile_bin, "little")
		
		i += 1

	f_in.close()
	f_out.close()
