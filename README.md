# Finn Property Analyser

[![Python Powered](https://www.python.org/static/community_logos/python-powered-w-100x40.png)](https://www.python.org)

Finn Property Analyser is a Python-based application for going through map locations on www.finn.no and collecting properties that fulfills a set of requirements, before the results are handled and stored into a Google spreadsheet.

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
py -3.5 main.py <auto>
```

**Parameters**

```<auto>``` auto is an optional parameter which loops the program to be executed four times a day by scheduling.

**Example**
```
py -3.5 main.py
py -3.5 main.py auto
```

## Property Results Sheets

Please contact me if you want access to the results; fredrik.bakken(at)gmail.com.
