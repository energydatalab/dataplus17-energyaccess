# Written for Duke Data+ 2017 Energy Access in Developing Countries team
# Developed by Ben Brigman
# email: bab2210@columbia.edu
# date: 7/26/17

import os
import json
import logging
import numpy as np
import rasterio
from rasterio.tools.mask import mask
import rasterio.merge as ramerge


# Configure logger
FORMAT = '%(asctime)s %(levelname)s:%(message)s'
DATEFMT = '%Y-%m-%d %H:%M:%S'
logging.basicConfig(filename='crop.log', level=logging.INFO, \
        format=FORMAT, datefmt=DATEFMT)

def main():
    logging.info('Starting crop_villages.py')

    ####### IMPORTANT: CHANGE VARIABLES BEFORE RUNNING #######
    run_merge = False
    run_crop = True
    run_stats = False#True
    stats_file = 'br_37_stats.json'
    boundaries_file = '../IndianVillagesDataset_DATA/ElectrificationMap_Bihar.geojson' # crop by bounding boxes


    ####### IMPORTANT: CHANGE IMAGES BEFORE RUNNING #######
    # Set list of images to merge (read from districts_img_list.txt)
    image_list = []
    prefix = '../IndianVillagesDataset_DATA/'
    with open('districts_img_list.txt','r') as openfileobject:
        for line in openfileobject:
            image_list.append(prefix+line.strip('\n')) # don't want '\n' at the end
    images = image_list
    print(images)

    ####### IMPORTANT: CHANGE BAND_NAMES BEFORE RUNNING #######
    # Set names of bands in images to loop through
    band_names = ['B1','B2','B3','B4','B5','B6','B7','B8','B9','B10','B11']
    metric_names = [' NDVI',' GIDX',' RAIN','VIIRS']
    month_names = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sept','Oct','Nov','Dec']
    for me in metric_names[:-1]:
        for mo in month_names:
            band_names.append(mo+me)
    band_names.append(metric_names[-1])
    print(band_names)

    # Load geojson with village information
    with open(boundaries_file) as gj:
        all_villages = json.load(gj)

    # Create image to crop from
    merged_img = 'merged/merged.tif'

    if run_merge:
        if not os.path.isdir('merged'): os.mkdir('merged')
        merge(images, merged_img)

    if run_stats:
        # Initialize dict to be written to json
        out_dict = {'village_info':[]}

    # Loop through villages in input json
    for info in all_villages['features']:
        village_geo = [info['geometry']]#np.array(info['geometry']['coordinates'])
        village_props = info['properties']
        village_id = village_props['CEN_2011']
        village_name = village_props['NAME']

        crop_img = 'Bihar(vil)-%s-%s.tif' % (village_name,village_id)

        if run_crop:
            crop(merged_img, village_geo, crop_img,"masked")
            village_geo[0]['coordinates'] = poly2rect(np.array(village_geo[0]['coordinates']))
            crop(merged_img, village_geo, crop_img,"cropped")

        if run_stats:
            band_stats = avg_bands(band_names, crop_img)
            village_stats = {'properties':village_props,
                    'statistics':band_stats}
            out_dict['village_info'].append(village_stats)

    if run_stats:
        logging.info('Preparing to write json')
        write_json(out_dict, stats_file)
        logging.info('json written')

    logging.info('crop_villages.py complete')

def merge(img_list, out_name):
    '''
        Takes a list of image file names and merges them into a single image

        Args:
            img_list -- a list of image file names to merge
            out_name -- the name of the output file to be written
    '''

    logging.info('Starting merge --- merging...')
    srcs=[]
    try:
        for img in img_list:
        	try:
        		srcs.append(rasterio.open(img))
        	except:
        		pass
    except:
        logging.error('Merge failed --- an image could not be opened')
        return

    out_img, out_transform = ramerge.merge(srcs)
    out_meta = srcs[0].meta.copy()
    out_meta.update({'driver':'GTiff',
                     'height':out_img.shape[1],
                     'width':out_img.shape[2],
                     'transform':out_transform})

    with rasterio.open(out_name, 'w', **out_meta) as dest:
        dest.write(out_img)

    logging.info('Finished merge')


def crop(big_img, bounds, out_name, option):
    '''
        Crops an image based on the provided polygon

        Args:
            big_img -- file name of the image to crop from
            bounds -- polygon giving crop boundaries
            out_name -- file name of the cropped image output
    '''
    out_name = option+'/'+out_name.replace("*","_")
    if not os.path.isdir(option): os.mkdir(option)

    logging.info('Starting crop %s ---cropping...' % out_name)
    with rasterio.open(big_img) as src:
        try:
            out_img, out_transform = mask(src, bounds, crop=True, all_touched=True)
            out_meta = src.meta.copy()
            if option=="masked":
                out_img = 255*np.array([np.sum(out_img.data, axis = 0, dtype=bool)]).astype('float32')
                out_meta.update({'count':1, 'dtype':'float32'})

        except ValueError:
            logging.error('Crop failed -- polygon error')
            return

    out_meta.update({'driver':'GTiff',
                     'height':out_img.shape[1],
                     'width':out_img.shape[2],
                     'transform':out_transform})
    with rasterio.open(out_name, 'w', **out_meta) as dest:
        dest.write(out_img)

    logging.info('Finished crop')


def write_json(feature, out_name):
    '''
        Writes the given information to a json

        Args:
            feature -- a dict containing the information to write
            out_name -- file name of the output file
    '''

    with open(out_name, 'w') as f:
        json.dump(feature, f, allow_nan=True)


def poly2rect(village_geo):
    '''
        Takes a polygon and returns the bounding box
    '''
    def updateCorners(extremes,poly):
        '''update the corner extremes'''
        xmin = min([item[0] for item in poly])
        extremes[0] = extremes[0] if extremes[0]<xmin else xmin
        xmax = max([item[0] for item in poly])
        extremes[1] = extremes[1] if extremes[1]>xmax else xmax
        ymin = min([item[1] for item in poly])
        extremes[2] = extremes[2] if extremes[2]<ymin else ymin
        ymax = max([item[1] for item in poly])
        extremes[3] = extremes[3] if extremes[3]>ymax else ymax

    def makeRect(extremes):
        '''takes corner extremes and returns the coordinates'''
        [xmin,xmax,ymin,ymax] = extremes
        return([[[xmin,ymin],[xmax,ymin],[xmax,ymax],[xmin,ymax]]])

    extremes = [np.nan]*4 #[xmin,xmax,ymin,ymax]
    for poly in village_geo:
        updateCorners(extremes,poly)
    return(makeRect(extremes)) #[[[xmin,ymin],[xmax,ymin],[xmax,ymax],[xmin,ymax]]]


def avg_bands(band_names, img_name):
    '''
        Takes input tiff image and returns dict with mean and variance
        of input image bands

        Args:
            band_names -- a list with n elements corresponding to a n-band
                image storing the keys to be associated with each band
            img_name -- string with the name of the image to be processed
    '''
    logging.info('Calculating statistics for %s' % img_name)
    try:
        img = rasterio.open(img_name)
    except:
        logging.warning('Image %s does not exist' % img_name)
        stats = 'Image does not exist'
        return


    stats = {el:[] for el in band_names}

    # Loop through bands, calculate stats, write to dict
    img_array = img.read()

    for band in range(img_array.shape[0]):
        band_array = img_array[band]
        # Mean and variance must be converted to python float for json
        mean = float(np.nanmean(band_array))
        variance = float(np.nanvar(band_array))

        stats[band_names[band]] = {'mean':mean, 'variance':variance}

    img.close()
    return stats

main()
