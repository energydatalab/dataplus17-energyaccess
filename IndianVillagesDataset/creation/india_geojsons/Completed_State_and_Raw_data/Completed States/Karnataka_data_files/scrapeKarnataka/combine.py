from xlrd import open_workbook
import os
import csv
import collections

def returnDirectory(source):
	wb = open_workbook(source)
	for s in wb.sheets():
		#print 'Sheet:',s.name
		values = []
		for row in range(s.nrows):
			col_value = []
			for col in range(s.ncols):
				value  = (s.cell(row,col).value)
				try : value = int(value)
				except : pass;
				col_value.append(value)
			values.append(col_value)
	return values



def combinePieces(pcfolder):
	if pcfolder == '': return {}
	toAdd = {}
	for f in os.listdir(pcfolder):
		p = open(pcfolder+'/'+f, 'r')
		pieceLines = csv.reader(p, delimiter=',')
		allLines = []
		for line in pieceLines:
			allLines.append(line)
		for i in range(1,len(allLines)):
			curLine = allLines[i]
			toAdd[int(curLine[6])] = ','.join(allLines[i])
	return toAdd

def updateKnown(roundFolder, ogSource):
	kfn = 'known.csv'
	if not (os.path.exists(kfn)):
		allElectrified = open(kfn,'w')
		allElectrified.write('MDDS STC,STATE NAME,MDDS DTC,DISTRICT NAME,MDDS Sub_DT,SUB-DISTRICT NAME,MDDS PLCN,Area Name,HH,eHH')
		allElectrified.close()

	existingValuesFile = open(kfn)
	existingLines = csv.reader(existingValuesFile, delimiter =',')
	eL = []
	for line in existingLines:
		eL.append(line)
	existingDict = {}
	for i in range(1,len(eL)):
		line = eL[i]
		existingDict[int(line[6])] = ','.join(line)

	toAdd = combinePieces(roundFolder)
	existingDict.update(toAdd)
	edSorted = collections.OrderedDict(sorted(existingDict.items()))

	allKnown = open(kfn,'w')
	allKnown.write('MDDS STC,STATE NAME,MDDS DTC,DISTRICT NAME,MDDS Sub_DT,SUB-DISTRICT NAME,MDDS PLCN,Area Name,HH,eHH')
	for key in edSorted:
		allKnown.write(edSorted[key] + '\n')

	allVillages = returnDirectory(ogSource)
	allDict = {}
	for arr in allVillages:
		allDict[arr[6]] = arr

	missingDict = allDict
	for key in edSorted:
		del missingDict[key]

	missingFile = open('unknown.csv', 'w')
	for key in missingDict:
		missingFile.write(','.join(str(e) for e in missingDict[key]))
		missingFile.write('\n')




