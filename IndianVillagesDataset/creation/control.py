import combine
import combine_garv_csv


# It is important to understand the file structure of this folder in order to understand how to run the function.
# This folder is split into 3 py files(control, combine, and combine_garv_csv) and data_files which contain folders that you need to input information into in order for the code to run.
# 	control.py			- calls functions from the other two files
#	combine.py			- creates a json file with 3 new properties, CEN_2011_ID(2011 Village Code), perc, eH, HH from Village ID/electriifcation information acquired from webscraping tool found in the file ID_webscraping
#	combine_garv_csv	- adds electrification data for more villages in json file after combine.py is called and adds the 3 properties for all villages that weren't found through the ID/electrification scraping tool. This function will work on its own if ID/electrification information isn't available for said village
#	data_files			- has two folders in directory. input files and output files. Input files and output files. The input files are where you place the raw data files in order to get geojson information for the output files. 
#	Completed_states	- look at the Completed_states to see what files go into input_files. 
#____________________________________________________________________________________________________	

combine.full_geojson_id_creation(['CEN_2001'])
combine_garv_csv.compile_geojson_id_with_csv_folder('curr_data_files/input_files/Garv_csv_scrape/Goa_folder/')


#There are two folders, input_files and output files that are in this directory. 

#The output files have the files geojson file and shape file that this program creates. 