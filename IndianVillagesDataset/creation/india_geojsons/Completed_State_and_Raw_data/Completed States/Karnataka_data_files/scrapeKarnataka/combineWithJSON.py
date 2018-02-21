import json
import shapefile
import geojson2shp
import os

def build0111Dictionary(convertFileName):
	convertLines = open(convertFileName, 'r')
	conversion = {}
	count = 0
	for line in convertLines:
		line = line[:-3]
		lineSep = line.split(';')
		try:
			idList = [lineSep[7],lineSep[8],lineSep[9],lineSep[5]]
			oldID = "%02d%02d%04d%08d" % (int(lineSep[7]), int(lineSep[8]),int(lineSep[9]),int(lineSep[5]))
			count += 1
			newID = lineSep[0]
			print (str(newID) + " from " + oldID + ", Completed: " + str(count))
			conversion[oldID] = newID
		except: continue
	return conversion

def build11ElecDictionary(allKnown):
	knowndict = {}
	known = open(allKnown, 'r')
	for line in known:
		line = line [:-1]
		lineSep = line.split(',')
		knowndict[lineSep[6]] = lineSep[8:10]
	return knowndict


def updateJSON(knowndict, translate, state):
	#for key, value in translate.items() :
		#print (key, value)
	totalKnown = 0
	for village in state["features"]:
		print (village["properties"]["CEN_2001"])
		if village["properties"]["LOC_2001"] in translate:
			village["properties"]["CEN_2011"] = translate[village["properties"]["CEN_2001"]]
		else:
			village["properties"]["CEN_2011"] = ''
		if (village["properties"]["CEN_2011"] in knowndict):
			village["properties"]["HH"] = knowndict[village["properties"]["CEN_2011"]][0]
			village["properties"]["eH"] = knowndict[village["properties"]["CEN_2011"]][1]
			village["properties"]["perc"] = str(float(village["properties"]["eH"])/float(village["properties"]["HH"]))
			totalKnown += 1
		else:
			village["properties"]["HH"] = ''
			village["properties"]["eH"] = ''
			village["properties"]["perc"] = ''
		print(village["properties"])
		print ("Total: " + str(totalKnown))
	return state

def cwj (translateName, mapjson, stateName):
	translateDict = build0111Dictionary(translateName)
	print()
	knowndict = build11ElecDictionary('known.csv')
	state = json.loads(''.join(open(mapjson,'r').readlines()))
	updated = updateJSON(knowndict, translateDict, state)
	print (updated["features"][1]["properties"])
	jsonText = json.dumps(updated)
	newJSONFile = open('electricityKnown.geojson','w')
	newJSONFile.write(jsonText)
	newJSONFile.close()

	gJ = geojson2shp.GeoJ('electricityKnown.geojson')

	# Creating a shapefile from the geoJSON object
	if not os.path.exists('shpFile'):
		os.mkdir('shpFile')
	gJ.toShp('shpFile/'+stateName)



