# Tools for Analytics Final Project: Squirrel Tracker
## Group Information
Team 80 Section 002
## Members: 
James Yang, Xinyue Li
Uni: jy3026, xl2917
## Description
This is the final project of Columbia IEORE4501 Tools for Analytics course. 
We build an application that can import the 2018 Central Park Squirrel Census data and sightings map, allowing the public to add, update, and view squirrels data.

## Features
### 1 Management Commands
#### Import
A command that used to import the data from the CSV file. 
The file path should be specified at the command line after the name of the management command as follows:
```
$ python manage.py import_squirrel_data /path/to/file.csv
```
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


## Link to server
