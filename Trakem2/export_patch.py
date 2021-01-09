import os

from ij import IJ, ImagePlus
from ij.process import FloatProcessor
from array import zeros
from random import random

from ini.trakem2 import Project
from ini.trakem2.display import Patch, Display

from ij.io import FileSaver


proj_list = ["/data/research/se/celegans/dataset3/N2DA_1430-2/L1/",
			"/data/research/se/celegans/dataset3/N2DA_1430-2/L2/",
			"/data/research/se/celegans/dataset3/N2DA_1430-2/L3/",
			"/data/research/se/celegans/dataset3/N2DA_1430-2/L4/",
			"/data/research/se/celegans/dataset3/N2DA_1430-2/L5/",
			"/data/research/se/celegans/dataset3/N2DA_1430-2/M1/",
			"/data/research/se/celegans/dataset3/N2DA_1430-2/M2/",
			"/data/research/se/celegans/dataset3/N2DA_1430-2/M3/",
			"/data/research/se/celegans/dataset3/N2DA_1430-2/M4/",
			"/data/research/se/celegans/dataset3/N2DA_1430-2/M5/",
			"/data/research/se/celegans/dataset3/N2DA_1430-2/N1/",
			"/data/research/se/celegans/dataset3/N2DA_1430-2/N2/"]


for i in range(len(proj_list)):

	data_dir = proj_list[i]
	proj_dir = os.path.join(data_dir, "montage_v1")
	img_dir = os.path.join(data_dir, "transformed")

	if not os.path.isdir(img_dir):
		os.makedirs(img_dir)

	proj_name =os.path.join(proj_dir, "montage_v1.xml")
	project = Project.openFSProject(proj_name)
	layerset = project.getRootLayerSet()

	layer_list = layerset.getLayers()
	
	fname_trans = os.path.join(data_dir, "transform.csv")
	fw = open(fname_trans, "w")
	for j in range(len(layer_list)):

		layer = layer_list[j]
		tiles = layer.getDisplayables(Patch)

		patches = layer.getDisplayables(Patch)

		
		for k in range(len(patches)):

			patch = patches[k]
			ip = patch.createCoordinateTransformedImage()
			imp = ImagePlus("", ip.target)

			box = ip.box
			fw.write("{}, {}, {}, {}, {}, {}\n".format(patch.title, int(layer.getZ()), box.x, box.y, box.width, box.height))

			fname = os.path.join(img_dir, patch.title)
			FileSaver(imp).saveAsTiff(fname)

	front = Display.getFront()
	front.close(project)
	fw.close()