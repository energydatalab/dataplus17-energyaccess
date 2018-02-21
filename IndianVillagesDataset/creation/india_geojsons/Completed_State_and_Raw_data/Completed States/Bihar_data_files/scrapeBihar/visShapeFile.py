from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib.patches import PathPatch
import math
import numpy as np

fig     = plt.figure()
ax      = fig.add_subplot(111)

map = Basemap(llcrnrlon=83,llcrnrlat=23.9,urcrnrlon=88.5,urcrnrlat=27.6,
			 resolution='i', projection='merc')

map.drawmapboundary(fill_color='silver')
# map.fillcontinents(color='#ddaa66',lake_color='aqua')
# map.drawcoastlines()

map.readshapefile('shpFile/bihar', 'comarques', drawbounds = False)

count = 0
overHalf = 0

percs = []
patches = []
# intervals = [[],[],[],[],[],[]]
# color =[(255,255,178),(254,217,118), (254,178,76), 'fd8d3c', 'f03b20', 'bd0026']
# numIntervals = len(intervals)-2
# percPerInt = 100/numIntervals

for info, shape in zip(map.comarques_info, map.comarques):
	patches.append(Polygon(np.array(shape), True))
	percs.append(float(info['perc']))
	# percentage = float(info['perc'])
	# if percentage < 1:
	# 	intervals[0].append(Polygon(np.array(shape), True))
	# 	continue
	# if percentage > 99:
	# 	intervals[len(intervals)-1].append(Polygon(np.array(shape), True))
	# 	continue

	# intNum = math.ceil(percentage/percPerInt)
	# intervals[intNum].append(Polygon(np.array(shape), True))

patchCol = PatchCollection(patches)
patchCol.set(array = np.asarray(percs), cmap = 'hot')
ax.add_collection(patchCol)
fig.colorbar(patchCol)
plt.show()