import os, re

import ini.trakem2.Project as Project
import ini.trakem2.display.Display as Display
import ini.trakem2.display.Patch as Patch
import ij.IJ as IJ
from java.awt import Rectangle



data_dir = "/data/research/se/celegans/dataset3/N2DA_1430-2/ex/"
proj_dir = os.path.join(data_dir, "montage")
img_dir = os.path.join(data_dir, "clahe")

## Create new project
project = Project.newFSProject("blank", None, proj_dir)
layerset = project.getRootLayerSet()


## Import tiles
# Get all layers
f = open(os.path.join(data_dir, "tile_location_valid.txt"), "r")

z_list = []
for l in f.readlines():

	elem = l[:-1].split(" ")
	fname = elem[0]
	xloc = int(elem[1])
	yloc = int(elem[2])
	zloc = int(elem[3])
	z_list.append(zloc) 
	
	imp = IJ.openImage(os.path.join(img_dir, fname))
	patch = Patch(project, imp.title, xloc, yloc, imp)
	patch.project.loader.addedPatchFrom(os.path.join(img_dir, fname), patch)
	
	layer = layerset.getLayer(zloc, 1, True)
	layer.add(patch)

f.close()

front = Display.getFront()
bounds = Rectangle(x=0, y=0, width=25000, height=25000)
front.resizeCanvas(bounds)

z_list.sort()
if z_list[0]!=0:
	layer = layerset.getLayer(0, 1, False)
	layer.remove(False)
	
# Save project
project.saveAs(os.path.join(proj_dir,"test.xml"), False)
front.close(project)
