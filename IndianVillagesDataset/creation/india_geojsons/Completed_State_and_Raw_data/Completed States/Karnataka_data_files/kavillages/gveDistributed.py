from xlrd import open_workbook
import numbers
from collections import deque
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path
import multiprocess as mp


def get_last_row(csv_filename):
    with open(csv_filename, 'r') as f:
        try:
            lastrow = deque(csv.reader(f), 1)[0]
        except IndexError:  # empty file
            lastrow = None
        return lastrow
    f.close()

def scrape(directory, start, end, processNum)
	intercsv = 'pieces/ec'+str(processNum)+'.csv'
	csvfile = Path(intercsv)
	if not csvfile.is_file():
		writeFile = open(csvfile, 'w')
		writeFile.write(",".join(values[0])+'\n')
		writeFile.close()
	lastID = -1
	lastLine = get_last_row(csvfile)
	if (lastLine[6]!='MDDS PLCN'):
		lastID = int(lastLine[6])
	print(lastID)
	print(csvFileName)
	for i in range(start, end):
		villID = int(directory[i][6])
		if (villID <= lastID): continue
		if (isinstance(villID, numbers.Number) and villID> 1000):
			print ('i:' + str(i) + ', ID:' + str(directory[i][6]))
			try:
				writeFile = open(intercsv, 'a')
				url = 'https://garv.gov.in/garv2/dashboard/village/'+str(villID)
				browser.get(url)
				wait = WebDriverWait(browser, 10)
				important = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".gridtotal")))
				totalhh = int(important.find_element_by_css_selector(".gridtotallabel+ .text-right").get_attribute('innerHTML'))
				totaleh = int(important.find_element_by_css_selector(".gridtotallabel+ .text-right + .text-right").get_attribute('innerHTML'))
				values[i].append(totalhh)
				values[i].append(totaleh)
				writeFile.write(",".join(str(e) for e in values[i])+'\n')
				print(values[i])
				writeFile.close()
			except:
				print('Mission Failed')
				writeFile.close()
				print()

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

	browser = webdriver.Chrome()
	values[0].append('HH')
	values[0].append('eHH')

#PARAMETERS
fileName = 'Rdir_2011_29_KARNATAKA.xls'
numThreads = 2
vilDirec = returnDirectory(fileName)


totalLines = len(vilDirec)
numLines = int(totalLines/numThreads)+1

count = 0
processes = []
for s in range(0,totalLines,numLines):
	if (s + totalLines > numLines):
		end = numLines
	else:
		end = s + totalLines
	process = mp.Process(target=scrape, args=(direc, s, end, count))
	processes.append(process)
	count++

for p in processes:
	p.start()




