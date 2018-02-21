import pyautogui
import time
import selenium
import csv
import os
import webbrowser

#### PLACE THIS FILE AND THE INDIA_FOLDER FILE IN DOWNLOADS FOLDER IN ORDER FOR IT TO WORK.
## Arguments:
#get_data(boolean, list)
#boolean set to true if you want it to write over existing data. (useful for updating electrification info)
#false only gets missing data. 
#list --> add names of states that need annotation. Useful if you only want info for a particular state.
		# leave empty if you want all the infomration


# Anywhere you see x=_____, y=_____, those are pixel coordinates specific to your computer. 
# These pixel coordinates are set for macboook pro 13in when the garv site is in full screen
# x___, y=_____, labels variables that need to be changed. Call mouse_position() function to find mouse_position at these following different locations. 
#info menu is the the drop down tab at the very left of the ALL INDIA title. The ALL INDIA title is found at the top of the page under disclaimer. 
# The info menu you need to click looks like a wide, v. If you click it, the All State, All District All Village tabs are visible. 
# remember to open Chrome in full screen before running script. 

#Mouse position locations that need to be changed for your computer. 
# type_search
info_menu = [1256,177]
all_state = [95,215]
all_district = [300,215]
# download. Scroll all the way down to the very bottom of the page and find location of the following
download_button = [58,718]
click_csv = [87,765]
delete_download_tab = [1262,777] #When you download something on chrome, a download tab pops up. Its important to delete it after it pops up. 

# scrolling
# this is super relative, but should work the same for all computers.
width_of_computer_screen = [1280]


type_search = False
mult = 6
def mouse_position():
	print(pyautogui.position())

def go_to_website(website):
	try:
		webbrowser.open(website)
		time.sleep(3*mult)
		pyautogui.click(x=info_menu[0], y=info_menu[1])
		time.sleep(0.25*mult)
		
	except:
		pyautogui.hotkey('command','w')

def get_list_info(country,state,district):
	rename_name = name_file(country,state,district)
	print(rename_name)
	if os.path.isfile(rename_name):
		with open(rename_name, 'rt', encoding='utf8') as csvfile:
			curr_csv_list = []
			csvreader = csv.reader(csvfile, delimiter=',')
			for counter, row in enumerate(csvreader):
				if counter>0 and row[0] is not 'Total':
					curr_csv_list.append(row[0]);
		return curr_csv_list
	else:
		type_enter(country,state,district)
		scroll_down()
		download(country,state,district)
		scroll_up()
		for filename in os.listdir("."):
			if filename.startswith("Garv"):
				os.rename(filename, rename_name)
		with open(rename_name, 'rt', encoding='utf8') as csvfile:
			curr_csv_list = []
			csvreader = csv.reader(csvfile, delimiter=',')
			for counter, row in enumerate(csvreader):
				if counter>0 and 'Total' not in row[0]:
					curr_csv_list.append(row[0]);
			del curr_csv_list[-1]
		return curr_csv_list

def name_file(country,state,district):
	prefix = country +'_folder/'
	rename_name = country
	if state is not '':
		rename_name = rename_name + "_" + state
		prefix = prefix + state + '_folder/'
	if district is not '':
		rename_name = rename_name + "_" + district
	rename_name = prefix + rename_name + '.csv'
	return rename_name


def type_enter(country,state,district):

	mini_scroll_up()
	if state == '' and district == '':
		pyautogui.click(x=all_state[0], y=all_state[1])
		pyautogui.typewrite("All")
	elif district == '':
		pyautogui.click(x=all_state[0], y=all_state[1])
		pyautogui.typewrite(state)
		global type_search
		type_search = True;
		pyautogui.typewrite(['enter'])
		time.sleep(.75*mult)
		pyautogui.click(x=all_district[0], y=all_district[1]+10)
		pyautogui.click(x=all_district[0], y=all_district[1])
		pyautogui.typewrite("All")
	else:
		global type_search
		if type_search == False:
			pyautogui.click(x=all_state[0], y=all_state[1])
			pyautogui.typewrite(state)
			global type_search
			type_search = True
			pyautogui.typewrite(['enter'])
			time.sleep(1*mult)
			pyautogui.click(x=all_district[0], y=all_district[1]+10)
		pyautogui.click(x=all_district[0], y=all_district[1])
		pyautogui.typewrite(district)
		pyautogui.typewrite(['enter'])
		time.sleep(1*mult)
	

def mini_scroll_up():
	time.sleep(0.1*mult)
	pyautogui.doubleClick(x=width_of_computer_screen[0], y=271);
	time.sleep(0.1*mult)
	pyautogui.mouseDown(x=width_of_computer_screen[0], y=271); 
	pyautogui.dragTo(width_of_computer_screen[0], 100, 1, pyautogui.easeInQuad)
	pyautogui.mouseUp();

def scroll_down():
	time.sleep(0.1*mult)
	pyautogui.click(x=width_of_computer_screen[0], y=212);
	time.sleep(0.1*mult)
	pyautogui.mouseDown(x=width_of_computer_screen[0], y=212);
	pyautogui.dragTo(width_of_computer_screen[0], 788, 1, pyautogui.easeInQuad)
	pyautogui.mouseUp();

def scroll_up():
	time.sleep(0.1*mult)
	pyautogui.doubleClick(x=width_of_computer_screen[0], y=575);
	time.sleep(0.1*mult)
	pyautogui.mouseDown(x=width_of_computer_screen[0], y=575); 
	pyautogui.dragTo(width_of_computer_screen[0], 100, 1, pyautogui.easeInQuad)
	pyautogui.mouseUp();

def download(country,state,district):
	if district is not 'Total':
		pyautogui.click(x=58, y=718)
		time.sleep(0.1*mult)
		pyautogui.click(x=87, y=765)
		time.sleep(0.1*mult)
		pyautogui.click(x=1262, y=777)



def get_list_info(country, state,district,only_missing_data):
	rename_name = name_file(country,state,district)
	print(rename_name)
	if os.path.isfile(rename_name) and only_missing_data:
		with open(rename_name, 'rt', encoding='utf8') as csvfile:
			curr_csv_list = []
			csvreader = csv.reader(csvfile, delimiter=',')
			for counter, row in enumerate(csvreader):
				try:
					if counter>0 and row[0] is not 'Total':

						curr_csv_list.append(row[0]);
				except:
					print('no info exception')
		return curr_csv_list
	else:
		type_enter(country,state,district)
		scroll_down()
		download(country,state,district)
		scroll_up()
		for filename in os.listdir("."):
			if filename.startswith("Garv"):
				os.rename(filename, rename_name)
		with open(rename_name, 'rt', encoding='utf8') as csvfile:
			curr_csv_list = []
			csvreader = csv.reader(csvfile, delimiter=',')
			for counter, row in enumerate(csvreader):
				if counter>0 and 'Total' not in row[0]:
					curr_csv_list.append(row[0]);
			del curr_csv_list[-1]
		return curr_csv_list

def get_data(only_missing_data, specific_states):
	#Variablesc

	mouse_position()
	country, state, district_name, past_district_list, past_village_list, = 'India', '', '', [], []
	#Gets state info
	go_to_website('https://garv.gov.in/garv2/dashboard/garv')
	try:
		os.stat(country + '_folder')
	except:
		os.mkdir(country + '_folder')
	states_list = get_list_info(country,state,district_name,only_missing_data)
	# Gets district info for each state
	for state in states_list:
		if state in specific_states or len(specific_states)==0:
			try:
				os.stat(country + '_folder/' + state + "_folder")
			except:
				os.mkdir(country + '_folder/' + state + '_folder')
			try:
				district_list = get_list_info(country,state,district_name,only_missing_data)
				for district in district_list:
					if 'Total' not in district_name:
						try:
							district_name = district
							village_list_curr = get_list_info(country,state,district_name,only_missing_data)
							if village_list_curr == past_village_list:
								os.remove(name_file(country,state,district_name))
							past_village_list = village_list_curr
						except:
							print("missing data for district(" + state + "_" + district_name + ")")
				district_name = ''
				global type_search
				type_search = False
			except:
				print("missing data for state(" + state + ")")





get_data(True, [])