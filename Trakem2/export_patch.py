from ij import IJ, ImagePlus
from ij.process import FloatProcessor
from array import zeros
from random import random

from ini.trakem2 import Project
from ini.trakem2.display import Patch, Display

from ij.io import FileSaver


# Open patches
project = Project.getProjects()[0]
layerset = project.getRootLayerSet()

front = Display.getFront(project)

layer = layerset.getLayers()[0]
tiles = layer.getDisplayables(Patch)

patches = layer.getDisplayables(Patch)

fname_trans = "/Users/jabae/Documents/montage/test_data/transform.csv"
fw = open(fname_trans, "w")
for i in range(len(patches)):

	patch = patches[i]
	ip = patch.createCoordinateTransformedImage()
	imp = ImagePlus("", ip.target)

	box = ip.box
	fw.write("{}, {}, {}, {}, {}, {}\n".format(patch.title, int(layer.getZ()), box.x, box.y, box.width, box.height))

	#fname = "/Users/jabae/Documents/montage/test_data/transformed/" + patch.title
	#FileSaver(imp).saveAsTiff(fname)

fw.close()