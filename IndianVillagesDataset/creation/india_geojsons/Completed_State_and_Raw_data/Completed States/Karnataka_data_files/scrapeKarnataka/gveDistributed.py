from xlrd import open_workbook
import numbers
from collections import deque
import csv
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path
import multiprocess as mp
from time import sleep


def get_last_row(csv_filename):
    with open(csv_filename, 'r') as f:
        try:
            lastrow = deque(csv.reader(f), 1)[0]
        except IndexError:  # empty file
            lastrow = None
        return lastrow
    f.close()

def scrape(directory, start, end, processNum):
	browser = webdriver.Chrome()
	midFolder = 'pieces'
	intercsv = midFolder+'/ec'+str(processNum)+'.csv'
	csvfile = Path(intercsv)
	if not (os.path.isdir(midFolder)):
		os.mkdir(midFolder)
	if not csvfile.is_file():
		writeFile = open(csvfile, 'w')
		writeFile.write(",".join(directory[0])+'\n')
		writeFile.close()
	writeFile = open(csvfile,'a')	
	lastID = -1
	lastLine = get_last_row(csvfile)
	if (lastLine != None and lastLine[6]!='MDDS PLCN'):
		lastID = int(lastLine[6])
	print(lastID)
	print(csvfile)
	print('start: ' + str(start))
	print('end: ' + str(end))
	for i in range(start, end):
		villID = directory[i][6]
		if (isinstance(villID, numbers.Number) and villID> 1000):	
			villID = int(villID)
			if (villID <= lastID): continue
			#print ('i:' + str(i) + ', ID:' + str(directory[i][6]), 'Process: ' + str(processNum))
			try:
				writeFile = open(intercsv, 'a')
				url = 'https://garv.gov.in/garv2/dashboard/village/'+str(villID)
				browser.get(url)
				wait = WebDriverWait(browser, 10)
				important = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".gridtotal")))
				totalhh = int(important.find_element_by_css_selector(".gridtotallabel+ .text-right").get_attribute('innerHTML'))
				totaleh = int(important.find_element_by_css_selector(".gridtotallabel+ .text-right + .text-right").get_attribute('innerHTML'))
				directory[i].append(totalhh)
				directory[i].append(totaleh)
				writeFile.write(",".join(str(e) for e in directory[i])+'\n')
				print('\nProcess: ' + str(processNum) + ', i: ' + str(i))
				print(directory[i])
				writeFile.close()
			except:
				print('Process: ' + str(processNum) + ', i: ' + str(i) + ', FAILED', end = ';')
				writeFile.close()
	print('EXITING')

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
				except : pass
				col_value.append(value)
			values.append(col_value)
	values[0].append('HH')
	values[0].append('eHH')
	return values

#PARAMETERS
fileName = 'Rdir_2011_10_BIHAR.xls'
numThreads = 6
vilDirec = returnDirectory(fileName)


totalLines = len(vilDirec)
numLines = int(totalLines/numThreads)+1

processes = []
arguments = []
finished = []
allDone = False
count = 0

for s in range(0,totalLines,numLines):
	if (s + numLines > totalLines):
		end = totalLines
	else:
		end = s + numLines
	arg = [vilDirec, s, end, count]
	process = mp.Process(target=scrape, args=arg)
	processes.append(process)
	arguments.append(arg)
	finished.append(False)
	count += 1

for p in processes:
	p.start()

while not allDone:
	for i in range(len(processes)):
		curProcess = processes[i]
		if not curProcess.is_alive() and finished[i] == False:
			processes[i] = mp.Process(target = scrape, args = arguments[i])
			processes[i].start()
			sleep(15)
			if not processes[i].is_alive():
				finished[i] = True
	allDone = True
	for b in finished:
		if not b:
			allDone = False


