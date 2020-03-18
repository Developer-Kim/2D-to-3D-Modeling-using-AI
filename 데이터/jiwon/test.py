import pptk
import numpy as np
import plyfile

data = plyfile.PlyData.read('Truck.ply')['vertex']

xyz = np.c_[data['x'], data['y'], data['z']]
rgb = np.c_[data['red'], data['green'], data['blue']]
v = pptk.viewer(xyz)
v.set(point_size=0.0005)
v.attributes(rgb / 255.)
