import gveDistributed2
import combine
import combineWithJSON as jcomb

#midFolder = 'round2'
#gveDistributed2.startProcess('unknown.csv', 2, midFolder)
#combine.updateKnown(midFolder, 'Rdir_2011_29_KARNATAKA.xls')
jcomb.cwj('ka_village_2011_2001_code_mapping.txt', 'ka.geojson', 'karnataka')