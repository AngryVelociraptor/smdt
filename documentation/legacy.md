Legacy Support
==============

One challenge involved with implementing a database like this is actually moving to it from an old system. 

To that end, the sMDT.legacy module contains functions for migrating from the old system. 

station_pickler class
---------------------
The station pickler class's job is to prepare data into a pickled tube file format from legacy systems that build CSVs.
There are four functions in station_pickler, one corresponding with swage, leak, darkcurrent, and tension stations. 
A function in this class pulls data from their respective data folders, and reformats it into a pickled tube.
It then archives the original csv file

Function | parameter | return | description
---|---|---|---
dict_to_tube(tubeDict)|tubeDict : dict()|Tube()|Takes a single dictionary representing a tube under our old system, and builds a tube object representing the same tube and perserving all data. #INCOMPLETE
tube_to_dict(tube)|tube : Tube()|dict()|The inverse of the above function, takes a tube object and builds a dictionary out of it for use with old applications. #ALSO INCOMPLETE