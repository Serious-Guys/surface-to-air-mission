# Surface to air mission
NASA Space Apps Challenge 2019 Project

## Description
Current project solves a problem which is determined by ambigious data taken from different satellite projects.
Main idea is about evaluating satellite data from NASA Aura mission and Copernicus Sentinel 5p using data fusion approach.
Data fusion allows to aggregate and match data taken by different space science missions.


## Modules

### Sentinel
This module is responsible for scrapping, downloading, normalizing and handling data acquired by copernicus satellites Sentinel 5p.
```wrapper.py``` contains a class which allows to retrieve data from open API.
```nchanlder.py``` is extended realisation of netCDF4 library which provides an opportunity to manipulate retrieved data more easily.


### NASA Earthdata
This module is doing same stuff as Sentinel but for NASA Aura mission.
```wrapper.py``` is an API wrapper for NASA's public interface.
```h5handler.py``` is handler for h5, he5 and hf5 files which are taken from NASA's GENDISC by wrapper.


### Ecocity
This module allows to retrieve and normalize data from Ukrainian public organization called Eco-City


### Model
Contains single file ```main.py``` which evaluates aggregated and already processed data with usage of Tensorflow ML library.
Later this model is integrated in web interface.


### Others stuff
Used for more convenient development. ```credentials.py``` for example is handling json file which contains creds for API's.


## Requirements
- Any OS
- Installed Python 3.6
- Shell environment
- Access to internet
- Accounts on NASA and Copencius services

## Installation
Simply run following commands (if you are using Linux):
- ```git clone git@github.com:Serious-Guys/surface-to-air-mission.git```
- ```cd surface-to-air-mission/```
- ```virtualenv .env```
- ```source .env/bin/activate```
- ```pip install -r requirements.txt```


## Contributors
- Vitaliy K. Oleg V. Andriy Z. Roman C.


## License
GNU GPL v3, feel free to distribute, contribute and share :)