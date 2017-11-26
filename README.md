# Finn Property Analyser

[![Python Powered](https://www.python.org/static/community_logos/python-powered-w-100x40.png)](https://www.python.org)

Finn Property Analyser is a Python-based application... TODO

## Installation

Install [Python 3.5.4](https://www.python.org/downloads/release/python-354/) and confirm the successful installation by running (in cmd):
```
py -3.5 --version
>>> Python 3.5.4
```

Open cmd, go to the project folder, and install the libraries by running:
```
py -3.5 -m pip install -r requirements.txt
```

## How to Run the Program

All commands described below can be ran from cmd.

### Running main.py
```
py -3.5 main.py <map-url>
```

**Parameters**

```<map-url>``` must be stated as a parameter since it defines which location to extract properties from (Make sure that the link is inside "").

**Example**
```
py -3.5 main.py "https://kart.finn.no/?lng=10.42324&lat=63.42024&tab=iad&zoom=13&mapType=normap&activetab=iad&searchKey=search_id_realestate_homes&keyword=&PRICE_FROM=&PRICE_TO=&ESTATE_SIZE%2FLIVING_AREA_FROM=&ESTATE_SIZE%2FLIVING_AREA_TO=&PLOT%2FAREARANGE_FROM=&PLOT%2FAREARANGE_TO=&NUMBER_OF_BEDROOMS_FROM=&NUMBER_OF_BEDROOMS_TO=&CONSTRUCTION_YEAR_FROM=&CONSTRUCTION_YEAR_TO=&ISNEWPROPERTY=&periode=&metro_distance_TO=&tram_distance_TO=&bus_distance_TO=&train_distance_TO=&orgId="
```