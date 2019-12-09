# Tools for Analytics
## Final Project: Squirrel Tracker
## Group Information
Team 80  Members: James Yang, Xinyue Li
## Summary
This is the final project of Columbia IEORE4501 Tools for Analytics course. 
Detailed Information: https://docs.google.com/document/d/1SPv3fMDKiemrR86rD-S9ecvI2npz3PljDzwCfxK2x5g/preview#

## Features
### 1 Management Commands
#### Import
A command that used to import the data from the CSV file. 
The file path should be specified at the command line after the name of the management command as follows:
```
$ python manage.py import_squirrel_data /path/to/file.csv
```
The squirrel census file can be downloaded here: 
https://data.cityofnewyork.us/api/views/vfnx-vebw/rows.csv

#### Export
A command that can be used to export the data in CSV format. 
The file path should be specified at the command line after the name of the management command as follows:
```
$ python manage.py export_squirrel_data /path/to/file.csv
```
### 2 Views
#### Map
A view that shows a map that displays the location of the squirrel sightings on an OpenStreets map. 
Located at: /map.
#### List
A view that lists all squirrel sightings with links to edit each. 
Located at: /sightings.
#### Update
A view to update a particular sighting. 
Located at: /sightings/<unique-squirrel-id>.
#### Add
A view to create a new sighting. 
Located at: /sightings/add.
#### Stats
A view with general stats about the sightings.
Located at: /sightings/stats.
