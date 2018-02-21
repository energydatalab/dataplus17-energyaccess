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


def returnDirectoryCSV(source):
	sourcefile = open(source, 'r')
	allLines = sourcefile.readlines()
	values = []
	for line in allLines:
		arr = line.split(',')
		for el in arr:
			try: el = int(arr)
			except: pass
		values.append(arr)
	values[0].append('HH')
	values[0].append('eH')
	return values

def scrape(midFolder, directory, processNum):
	print('directory:')
	print(processNum)
	browser = webdriver.Chrome()
	intercsv = midFolder+'/ec'+str(processNum)+'.csv'
	csvfile = Path(intercsv)
	if not (os.path.isdir(midFolder)):
		os.mkdir(midFolder)
	if not csvfile.is_file():
		writeFile = open(csvfile, 'w')
		writeFile.write('MDDS STC,STATE NAME,MDDS DTC,DISTRICT NAME,MDDS Sub_DT,SUB-DISTRICT NAME,MDDS PLCN,Area Name,HH,eHH\n')
		writeFile.close()
	
	#Find Last ID
	lastID = -1
	openFile = open(csvfile,'r')
	lastLine = openFile.readlines()[len(openFile.readlines())-1].split(',')
	try: lastId = int(lastLine[6])
	except: pass
	openFile.close()
	startIndex = 1
	while (lastID != -1 and ids[startIndex-1] != lastID): startIndex += 1 #Get to Starting Index

	for villArr in directory[startIndex:]:
		print(villArr)
		try: villID = int(villArr[6])
		except: continue
		if (villID> 1000):	
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
				print('\nProcess: ' + str(processNum))
				print(directory[i])
				writeFile.close()
			except:
				print('Process: ' + str(processNum) + ', FAILED', end = ';')
				writeFile.close()
	browser.quit()
	print('EXITING')


def startProcess(source, threads, midFolder):
	#PARAMETERS
	vilDirec = returnDirectoryCSV(source)
	totalLines = len(vilDirec)
	numLines = int(totalLines/threads)+1

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
		arg = [midFolder, vilDirec[s:end], count]
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
				break


