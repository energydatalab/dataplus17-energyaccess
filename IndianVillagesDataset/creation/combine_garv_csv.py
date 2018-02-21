# This file works with the geojson created using the village ids only and then adds in extra information 
# found through the Garv download button. 

import json
import csv
from os import listdir
from os.path import isfile, join
import os
#Copy the garv file with all of the csvfiles for the district into input_files/Garv_csv_scrape. This code is useful
#if you have all of the ID data for the state, and created the geojson with all of the electrification info for id data
def iterate_csv_district_files(mypath):
	list_files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
	return list_files;





def compile_geojson_id_with_csv_folder(csvfolder_path, json_path):
	count=0
	list_files = iterate_csv_district_files(csvfolder_path)
	state_with_suffix = list_files[0].split('_')[1]
	state_name = state_with_suffix.split(".csv")[0]
	print(state_name)
	with open(json_path) as data_file:
		data = json.load(data_file)
		for i in data['features']:
			if i['properties']['perc'] == -1:
				district_name = i['properties']['DISTRICT']
				csv_file_name = "India_" + state_name + "_" + district_name + ".csv"
				if csv_file_name in list_files:
					village_list = extract_unique_village_names_GARV_csv(csvfolder_path,csv_file_name)
					village_dic  = extract_electrification_data(csvfolder_path,csv_file_name,village_list)
				try: 	
					i['properties']['perc'] = village_dic[i['properties']['NAME']][0]
					i['properties']['HH'] = village_dic[i['properties']['NAME']][1]
					i['properties']['eHH'] = village_dic[i['properties']['NAME']][2]
					print(i['properties']['perc'])
					count+=1

				except:
					ph=1

	open(json_path, "w").write(json.dumps(data,indent =1))





def extract_unique_village_names_GARV_csv(csvfolder_path,csvfile):
	village = {}
	count = 0
	unique_village = []
	village_unique = {}

	with open(csvfolder_path + csvfile, 'r', encoding='utf8') as csvfile:
		csvreader = csv.reader(csvfile, delimiter=',')
		for counter, row in enumerate(csvreader):
			if counter>0:
				if row[0] in village:
					village[row[0]]+=1

				else:
					village[row[0]]=1
		for key in village:
			if village[key] == 1:
				count+=1
				unique_village.append(key)
	
	return unique_village

def extract_electrification_data(csvfolder_path,csvfile,unique_village):
	village_elec_unique = {}

	with open(csvfolder_path + csvfile, 'r', encoding='utf8') as csvfile:
		csvreader = csv.reader(csvfile, delimiter=',')
		for counter, row in enumerate(csvreader):
			if counter>0:
				if row[0] in unique_village:
					village_elec_unique[row[0]] = [row[10],row[7],row[8]]
	return village_elec_unique

