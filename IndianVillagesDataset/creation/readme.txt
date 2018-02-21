Datameet_Summary_Readme

Read this file, if you want to create Shapefiles and geojson files from the electrification and boundries data available for villages.  At the very bottom of the document, under the title "Data used", I will explain the importance of each band of data that we are using. 

The purpose of this document is to outline the steps necessary to use the Electrification data acquired from the garv database. (https://www.garv.gov.in) and the village shapefiles located in the datameet public data-website. 

General Summary of what Indian_GT_Data contains: 
	1. This folder has processed geojson ground truth data files for the states, Bihar, Karnataka, Gujarat, Kerala, and Goa. These processed geojson files have electrification 	data and boundary data for most of the villages in each of the states.
	2. This folder contains code to create the processed geojson file if given the following information (electrification data for each village, geojson data)
	3. This folder contains code to acquire electrification data for every state in India.
	4. This folder contains code to visualize geojson ground truth data for each state. 
	In the following section (Folder Structure of Indian_GT_Data, I will explain how the files are organize to accomplish the 3 tasks shown above. 





Folder Structure of Indian_GT_Data:

	1. Completed_State_and_Raw_data:	
		- Completed States: Has completed geojson information for each state in the folder
		- Raw Data	    : Has the raw geojson information that was used to create the Completed States Folder
	
	2. Scrape_Code_and_files: 
		- csv_scrape	    : scrapes data using the download button information in the website garv.gov.in. Run to see how it works. 
		- id_scrape	    : uses the different urls for each indian village id to extract the electrification data.
		- Look at the section (Two Data Sources for more information on this process)
	
	3. curr_data_files	    : where to put raw data files (geojson data, id information, csv scrape data, id scrape data
		- remember to empty all the folders and add your states information. Look at Raw Data Files for more information about the raw data files required. 

	4. pycache		    : disregard this file
	5. control.py		    : file that combines all the code from other files to create processed geojson files
	6. combine.py		    : adds the electrification data from the id_scrape data to the raw geojson file
	7. combine_garv_csv.py	    : adds the electrification data from csv_scrape to the geojson file
	8. geojson2shp.py	    : converts the geojson file to shp file
	9. visShapeFile.py	    : visualizes the shp file





Raw Data Files:
	File 1: Name ex: gj.geojson geojson file with shape information for each village(Each geojson has properties for each village. These properties vary for each json file!!! This needs to be edited)
	File 2: Name: ex: gj_village_2011_2001_code file that comes with geojson file. This has the 2011 Village ID and the information needed to form the 2001 Census ID. 
	~File 3: Name: ex:geojson_elec_id.json. Final geojson file with all the electrified shape information for ID locator. The villages with missing file information is has a perc electrification value of -1.


Two Data-sources:

Garv Database: The Garv database is a public government website that has decently accurate data for electrification, total households, and electrified householdss for each villages. We are able to acquire the data from the Garv Database through 2 main methods. Link: https://garv.gov.in/garv2/dashboard/garv

1. The garv website has a seperate url for each Village. The website url for each Village is distinguished by their 2011 ID. (ex: a possible Garv page for a village would be https://garv.gov.in/garv2/dashboard/village/092444. There is a tool that can extract the village information from each village in India. The location of this tool will be provided to you.The contents of this csv file will have the id for each village coupled with the electrification percentage, district, subdistrict and state. 
Drawback: the code for scraping the website data requires5 parallel processing units on a computer and takes about a week of continuous running to get all of the data for India. 

2. The garv website also has an option to download electrification data at the state level where it allows you to manually download a csv with the avg electrification for each district in the state. The data is also available district level where it allows you to manually download a csv with electrification data for each village in the district. 
Drawbacks: Much faster than ID verificatoin. Takes a few hours. The csv data doesn't contain Village IDs so any village with a duplicate name has to be removed. 



Questions:

1. Why do we need geojsons with electrification data?
	This is important to the project because it ground truth data to train a classifier to distinguish between regions with electricity and regions without electricity. 

2. What data are we sending with this groundtruth data
The data we are using with this groundtruth shapefile is NDVI/Green/Rainfall/Viirs Data that give information on how irrigated an area is.

	Data used:
	We plan on feeding the algorithm 12 bands of NDVI, Green, and Rainfall data (1 for every month of the year because its hard for the NDVI and Green index to tell an irrigated land from an unirrigated land during monsoon season because all cropland looks well irrigated then. 

	NDVI:(12 bands) A measurement index of whether a targeted area has crops or not. Can distinguish between regions that are forest land, deserts, cities and irrigated fields. We plan on using the irrigated field data. 
	((red-infrared)/(red+infrared))

	Green(12 bands): Similar to NDVI except it measures stress level of a crop. Formula to calculate it (green band/infrared band)

	Rainfall(12 bands): Gives information of how rainfed the crops are. 

	VIIRS(1 band): Lights at Night Data. 1 km resolution

3. What is a brief summary of how we are planning on trainig a classifier with these datasets?

	Our Solution: We plan on combining the data acquired by ID url and the data acquired by the download button and creating a compiled csv of all of the villages and their electrification information. This csv is then combined with the geojson of all the village boundries so we can visualize the electrification information and use the data as groundtruth for training an electrification data map. 
