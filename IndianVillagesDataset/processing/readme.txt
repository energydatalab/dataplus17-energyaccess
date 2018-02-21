merge_crop.py takes image tiles creating a region, merges them together,
creates cropped images corresponding to the provided locations,
and then calculates the mean and variance of each band in each location. 

Dependencies:
	--python3
	--json
	--logging
	--numpy
	--rasterio

We recommend that you use a virtual environment (such as anaconda) so that
the installations do not interfere with your base python installation.

This code was developed in an anaconda environment running python3.5.

The code as written is designed to merge image tiles containing agricultural
indices, crop around village locations, then calculate the mean and variance
of the indices for that village.

main():
	Set images to contain a list of the file names of images you want to
	merge (you can automize this processs by running getImgList.py)

	Set merged_img to contain a string with the file 
	name of the merged image output

	Set run_merge = True if you want to merge the images

	Set run_crop = True if you want to crop the images

	Set run_stats = True if you want to calculate mean and variance of
	the images

	Set stats_file to contain a string with the file name of the output
	if running stats

	Set boundariesFile to contain a string with the file name of the 
	geojson containing polygon boundaries to crop

	Set crop_img to contain a string with the file name of the cropped
	image
	    NOTE: the file is set to loop and create many crops. Your name
		  choice should reflect this.



