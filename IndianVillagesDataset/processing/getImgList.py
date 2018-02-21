"""
getImageNameList.py 
gets the names of all multi-band images stored in /IndianVillagesDataset_DATA
and generates a .txt file with each line being an image name.

@author: Boning Li
Created on Sun Jul 30 22:26:22 2017
"""
import os

rname = os.path.dirname(os.path.realpath(__file__))
dname = os.path.join(rname,'../IndianVillagesDataset_DATA')
fnames = next(os.walk(dname))[2]
name_list = []

for fname in fnames:
    if fname[-3:] == 'tif':
        name_list.append(fname)
name_list.sort()
print(name_list)

with open('districts_img_list.txt','w') as outfile:
    outfile.write("\n".join(name_list))
        
print(len(name_list))
