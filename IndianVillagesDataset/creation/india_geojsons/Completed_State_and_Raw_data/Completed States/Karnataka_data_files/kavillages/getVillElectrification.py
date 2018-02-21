from xlrd import open_workbook
import numbers
from collections import deque
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_last_row(csv_filename):
    with open(csv_filename, 'r') as f:
        try:
            lastrow = deque(csv.reader(f), 1)[0]
        except IndexError:  # empty file
            lastrow = None
        return lastrow
    f.close()

csvFileName = 'electrification.csv'
lastLine = get_last_row(csvFileName)
lastID = int(lastLine[6])
print(lastID)


wb = open_workbook('Rdir_2011_29_KARNATAKA.xls')
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

from pathlib import Path

my_file = Path(csvFileName)
if not my_file.is_file():
	writeFile = open(csvFileName, 'w')
	writeFile.write(",".join(values[0])+'\n')
	writeFile.close()

writeFile = open(csvFileName,'a')

for i in range(1, len(values)):
	villID = int(values[i][6])
	if (villID <= lastID): continue
	if (isinstance(villID, numbers.Number) and villID> 1000):
		print ('i:' + str(i) + ', ID:' + str(values[i][6]))
		try:
			url = 'https://garv.gov.in/garv2/dashboard/village/'+str(villID)
			browser.get(url)
			wait = WebDriverWait(browser, 10)
			important = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".gridtotal")))
			totalhh = important.find_element_by_css_selector(".gridtotallabel+ .text-right").get_attribute('innerHTML')
			totaleh = important.find_element_by_css_selector(".gridtotallabel+ .text-right + .text-right").get_attribute('innerHTML')
			print(type(totalhh))
			values[i].append(totalhh)
			values[i].append(totaleh)
			writeFile.write(",".join(str(e) for e in values[i])+'\n')
			print(values[i])
		except:
			print('Mission Failed')
			print()
writeFile.close()


