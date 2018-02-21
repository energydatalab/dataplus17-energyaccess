import gveDistributed2
import combine
import combineWithJSON as cwjson

midFolder = 'round2'
gveDistributed2.startProcess('unknown.csv', 2, midFolder)
combine.updateKnown(midFolder)
cwjson.cwj('bh_village_2011_2001_code_mapping.txt', 'br.geojson', 'bihar')