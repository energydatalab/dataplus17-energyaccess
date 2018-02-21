from xlrd import open_workbook
import os
import csv
import collections
import sys
import json
from os import listdir
from os.path import isfile, join



# Very important information:
# Census Village 2001_id = state + district + subdistrict + village [results in 16 digit number]
# (2 digits) state = if number is 1 digit, represent as 0+digit. 
# (2 digits) district = if number is 1 digit, represent a 0+digit
# (4 digits) subdistrict = number + 0s until 4 digits are met.
# (8 digits) village = number + 0s until 8 digits are met. 


# Scraping the garv electrification website using the village ids creates 5 seperate csv files.
# A file for each processing unit that runs webscraping tool. This function combines csv files into 1 file. 

# Arguments:
# pcfolder				-	the folder that contains 5 seperate csv files.		(ex: 
# destination_folder	-	folder of combined csv file
# [ex:combine.combinePieces('curr_data_files/input_files/id_scrape_pieces/pieces','curr_data_files/input_files/id_scrape_compiled')]

# About output file:
# A column in this csv file is for 2011 ID***.
def combinePieces(pcfolder,destination_folder):
	writetitle = True
	with open(destination_folder + '/combined.csv', 'w') as csvcomfile:
		csvwriter = csv.writer(csvcomfile, delimiter = ',')

		for f in os.listdir(pcfolder):
			with open(pcfolder+'/'+f, 'r') as csvfile:
				spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
				for counter,row in enumerate(spamreader):
					if writetitle ==True or counter>1:
						csvwriter.writerow(row)
						writetitle = False;
#______________________________________________________________________________________________________________

# The geojson file downloaded from datameet doesn't have 2011 ID. The geojson either has a property that 
# contains the 2001 Village ID or has the information required to create the 2001 Village ID. A textfile 
# that is provided with geojson file has 2001 ID and 2011 ID. With this, I can add a property to Geojson 
# file with 2011 ID, and 2001 ID. 
# This method adds both fields to geojson. 
# !!!THE FORMULA TO CREATE THE 2001 VILLAGE ID IS 2001_id = state + district + subdistrict + village. 

# Arguments:
# jsonfile 					-	name and directory of the jsonfile that is raw from datameet website
# txtfile 					-	name and directory of the txtfile that has the linking 2001 and 2011 ID information
# jsonfile_id_properties	-	Each json object in geojson has data['features'] and data['geometry']. list the properties that make up 2001 Village Census ID not 
							   #including the data['features']. If a seperate property that has 2001 Village ID exists, just put it as the only value in the list. For example if there is a property in the geojson with the 2001 Village ID called CENSUS_CODE_2001, 
							   #instead of writing data['features']['properties']['CENSUS_CODE_2001'], just write 'CENSUS_CODE_2001'. Look at example below if you are confused. 
# txtfile_id_properties		-	list of columns that make up 2001 Village Census ID in the order of the formula. If a seperate property that has 2001 Village ID exists, just put it as the only value in the list. 
# ex: add_ids_to_json('curr_data_files/input_files/geojson_raw/gj.geojson','curr_data_files/input_files/village_id_text_file_raw/gj_village_2011_2001_code_mapping.txt',['CENSUS_CODE_2001'], )

def add_ids_properties_to_json(jsonfile,txtfile,jsonfile_id_properties):
	txtfile_add_2001_id(txtfile,txtfile_id_properties)



# The textfile has multiple columns that contain information that allow you to figure out the 2001 CEN ID. This file use those columns to create CEN2001 ID and save into another column in folder. 
#It will then save this edited file into a csv in the desired folder. (output_file/edited_2001_2011_id_file)
def txtfile_add_2001_id(textfile_folder,destination_folder):
	onlyfiles = [f for f in listdir(textfile_folder) if isfile(join(textfile_folder, f))]
	txtfilename = ""
	for file in onlyfiles:
		if ".txt" in file:
			txtfilename = file;
	if len(onlyfiles) == 0: 
		with open(destination_folder + csvfilename, 'w+'):
			f.close()
	else:	
		crs = open(textfile_folder + '/' + txtfilename, "r")
		digits_per = {'state2001': 2, 'district2001': 2, 'sub_district2001': 5, 'village2001': 8}
		csvfilename = 'combined.csv'

		f = open(destination_folder + csvfilename, 'w+')
		f.close()

		with open(destination_folder + csvfilename, 'a') as csvcomfile:

			csvwriter = csv.writer(csvcomfile, dialect='excel')

			for counter, row in enumerate(crs):
				row_split = row.split(';')
				state_code_2001 = str(row_split[7])
				district_code_2001 = str(row_split[8])
				sub_district_code_2001 = str(row_split[9]).split('\t\n')[0]
				village_code_2001 = str(row_split[5])

				if counter==0:

					row = "".join(row.split())
					row_split1 = row.split(';')
					row_split1.append('CEN2001_ID')
					csvwriter.writerow(row_split1)
				if counter>1:
					row = "".join(row.split())
					row_split = row.split(';')
					if len(state_code_2001)==1: state_code_2001 =	'0' + state_code_2001		
					for x in range(0,digits_per['state2001']-len(state_code_2001)):
						state_code_2001 = state_code_2001 + '0'

					if len(district_code_2001)==1: district_code_2001 =	'0' + district_code_2001
					for x in range(0,digits_per['district2001']-len(district_code_2001)):
						district_code_2001 = district_code_2001 + '0'

					for x in range(0,digits_per['sub_district2001']-len(sub_district_code_2001)):
						sub_district_code_2001 = '0' + sub_district_code_2001

					for x in range(0,digits_per['village2001']-len(village_code_2001)):
						village_code_2001 = '0' + village_code_2001 
					CEN2001 = state_code_2001 + district_code_2001 + sub_district_code_2001 + village_code_2001
					CEN2001 = "".join(CEN2001.split())
					row_split.append(str(CEN2001))
					csvwriter.writerow(row_split)
	return csvfilename
# Uses csv file created in txtfile_add_2001_id() method to create the CEN_2011_ID property in geojson file. 
def add_2011_id_to_json(csvfile,jsonfile_folder,json_2001_propname):
	d_2001_2011 = {}
	count = 0
	with open(csvfile) as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
		for counter,row in enumerate(spamreader):
			if counter>1:
				try:
					count+=1
					d_2001_2011[row[10]] = row[0]
				except:
					nothing = 1
	onlyfiles = [f for f in listdir(jsonfile_folder) if isfile(join(jsonfile_folder, f))]
	jsonfilename = ""
	for file in onlyfiles:
		if '.json' in file or '.geojson' in file:
			jsonfilename = file
			print(jsonfilename)
	with open(jsonfile_folder + '/' + jsonfilename) as data_file:
		data = json.load(data_file)
		for i in data['features']:
			try:
				i['properties']['CENSUS_2011_DATA'] = d_2001_2011[i['properties']['CEN_2001']];
			except:
				i['properties']['CENSUS_2011_DATA'] = -1
	return data

# Combines electrification id information with json file.
def combine_electrification_id_with_json(json_data, csvfile, json_destination):
	d_2011_eHH = {}
	d_2011_HH = {}
	counters=0
	count=0
	with open(csvfile) as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
		for counter,row in enumerate(spamreader):
			if counter>1:
				try:
					d_2011_eHH[row[6]] = row[9]
					d_2011_HH[row[6]] = row[8]
				except:
					ph=1
		for i in json_data['features']:
			try:
				i['properties']['eHH'] = d_2011_eHH[i['properties']['CENSUS_2011_DATA']];
				i['properties']['HH'] = d_2011_HH[i['properties']['CENSUS_2011_DATA']];
			except:
				count+=1
				i['properties']['eHH'] = -1;
				i['properties']['HH'] = -1;

			try:
				i['properties']['perc'] = float(d_2011_eHH[i['properties']['CENSUS_2011_DATA']])/float(d_2011_HH[i['properties']['CENSUS_2011_DATA']])*100
			except:
				counters+=1
				i['properties']['perc'] = -1





	open(json_destination, "w").write(json.dumps(json_data,indent =1))

def full_geojson_id_creation(jsonfile_name,json_properties):	
	combinePieces('curr_data_files/input_files/id_scrape_pieces/pieces/','curr_data_files/input_files/id_scrape_compiled/')
	csvfilename = txtfile_add_2001_id('curr_data_files/input_files/village_id_text_file_raw/', 'curr_data_files/output_files/edited_2001_2011_id_file/')
	json_data = add_2011_id_to_json('curr_data_files/output_files/edited_2001_2011_id_file/combined.csv' , 'curr_data_files/input_files/geojson_raw/', json_properties)
	combine_electrification_id_with_json(json_data, 'curr_data_files/input_files/id_scrape_compiled/combined.csv' , 'curr_data_files/output_files/geojson_processed/geojson_elec_id.json')






