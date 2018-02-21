# Electricity Access in Developing Countries
## WHERE IS THE DATA
_BEFORE EVERYTHING IS PUBLISHED ON FIGSHARE, PLEASE FIND THEM HERE:_

### US Power Plant Data
* __VM__ (1 - raw data; 2 - processed dataset):
  1. Z:\\data\\energyaccess\\US_Power_Plants_RAW_NAIP.tar<br/>
  Z:\\data\\energyaccess\\US_Power_Plants_RAW_LS8.tar
  2. Z:\\data\\energyaccess\\dataplus2017\\USPowerPlantDataset\\USPowerPlantDataset_DATA\\
* __GPU__ (dataset only): /home/hyperion/dataplus/dataplus2017/USPowerPlantDataset/USPowerPlantDataset_DATA/

### Indian Villages Data
  Either of the following holds the COMPLETE __multi-band imagery__ & __electrification map__ of Bihar, India.
* __VM__ (1 - compressed; 2 - extracted for test and review): <br/>
  1. Z:\\data\\energyaccess\\archive\\IndianVillagesDataset_DATA.zip<br/>
  2. Z:\\data\\energyaccess\\dataplus2017\\IndianVillagesDataset\\IndianVillagesDataset\_DATA\
* __GPU__ : NA


## WHAT ARE THE SETS LIKE
This section introduces the organization of each set of products, including data and code.

### US Power Plants\* - A list of files
\* More info: for __data__, please see the dataset documentation [here]( https://github.com/energydatalab/dataplus2017/blob/master/USPowerPlantDataset/USPowerPlantDataset_DATA/README.md), for __code__ the creation demo [here](https://github.com/bl166/USPowerPlantDataset/blob/master/README.md).

#### __Data__
* /USPowerPlantDataset_DATA
  * /uspp\_naip - __naip\_ID\_StateName\_FuelCategory.tif__
  * /uspp\_landsat - __ls8\_ID\_StateName\_FuelCategory.tif__
  * /exceptions ```// none of accepted annotations marks it as containing a power plants```
  * /annotations ```// polygons in .txt, and rasterized annotations in binary and confidence maps .png```
    * accepted_ann_json.txt ```// accepted annotations condensed```
    * /binary - __bilabels\_ID.png__
    * /confidence - __conflabels\_ID.png__
  * uspp_metadata.geojson ```// power plants metadata```
  * [README.md]( https://github.com/energydatalab/dataplus2017/blob/master/USPowerPlantDataset/USPowerPlantDataset_DATA/README.md) ```// data explanations```
* /USPowerPlantDataset_RAW
  * US\_Power\_Plants\_RAW\_NAIP.tar.gz
  * US\_Power\_Plants_RAW\_LS8.tar.gz

#### Code
  * /USPowerPlantDataset\_CREATION
    * \*A SUBSET OF USPowerPlantDataset\_DATA\* (ID=300\~500)
    * egrid2014\_data\_v2\_PLNT14.xlsx ```// a subset of the egrid document```
    * P1DATAPREP_cropPowerPlants.py ```// prepares data - download```
    * P1DATAPREP\_fixLs.m ```// prepares data - preprocess```
    * P2ANNOGEN\_getAllAcceptedCondensed.py ```// fetches annotations```
    * P3DATAPROC\_make.py ```// constructs dataset```
    * P3DATAPROC\_report.py ```// displays data distribution```
    * P4TESTCLSFR\_classify\_sample.py ```// tests classifiers```
    * [README.md](https://github.com/bl166/USPowerPlantDataset/blob/master/README.md) ```// documentation```

### Indian Villages Data \* - A list of files
\* More info: for __data__, please see data description [here](https://github.com/energydatalab/dataplus2017/blob/master/IndianVillagesDataset/README.md), for __code__ the creation summary [here](https://github.com/energydatalab/dataplus2017/blob/master/IndianVillagesDataset/creation/readme.txt).
#### __Data__
* /IndianVillagesDataset\_DATA ```// size: 45,220 ```
  * imagery/  ```// 48-band imagery by village bounding boxes```
    * Naming: __StateName(type)-VillageName-6DigitCensusID.tif__ \*
  * masks/ ``` // binary masks of village bounding polygons```
    * Naming: __StateName(type)-VillageName-6DigitCensusID.tif__ \*
  * ElectrificationMap_Bihar.geojson ```// electrification map (of Bihar); i.e. ground truth from garv & village boundaries```

#### Code
  * /creation
    * /india\_geojsons ```// Indian administrative divisions .geojson```
    * makeIrriElecMetrics.js ```// exports composite imagery from GEE```
    * /Scrape_code_and_files ```// download village info from garv.gov.in```
      * /csv_scrape ```// uses the download button```
      * /id_scrape ```// uses the village IDs```
    * /curr_data_files ```// current data```
    * combine.py
    * combine_garv_csv.py
    * control.py
    * geojson2shp.py
    * visShapeFile.py
    * [readme.txt](https://github.com/energydatalab/dataplus2017/blob/master/IndianVillagesDataset/creation/readme.txt) ```// creation code documentation```
  * /processing
    * merge\_crop.py ```// merges or crops given image(s)```
    * getImgList.py ```// generates districts_img_list.txt```
    * genSamples.m ```// generate sample images```
    * [readme.txt](https://github.com/energydatalab/dataplus2017/blob/master/IndianVillagesDataset/processing/readme.txt) ```// documentation for merge_crop.py```
