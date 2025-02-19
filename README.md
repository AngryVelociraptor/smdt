MSU sMDT Python Package
![](https://atlas.cern/sites/atlas-public.web.cern.ch/files/inline-images/ATLAS-Logo-Ref-RGB-H-transparent.png)
========

smdt is the Python package built to provide an organized object oriented data structure for applications used in the MSU ATLAS sMDT lab. 
It will also provide a consistent interface for any interactions with the database. 

Structure
--------
Fig. 1
![Fig. 1](https://i.imgur.com/g7Dv28C.png)
Key:

-Each box is a class

-Arrows represent an "is a" relationship, inheritance. A LeakStation is a type of *Station*

-Italic class names represent an abstract class that should be initialized

-The lines with black diamonds at the end represent a "has a" or an "is made up of" relationship. The numbers represent the multiplicity of the side of the relationship. These are usually member variables.

-A Tube has 1 LeakStation object

-A Leakstation object has a list of LeakRecords 

-The colored boxes in the background represent the python packages (folders) that the modules are in. 

-Practically, that means you just write `from sMDT import tube` or `from sMDT.data import swage`

Documentation
-------------
Full documentation can be found in [our documentation folder](documentation/home.md)

Installation
------------
Visit the following link for the source code.

https://github.com/dravinflores/smdt

As of now, this library is not uploaded to PyPi or a similar python package manager for easy installation with like `pip install sMDT`.
Maybe it will be eventually, but for now you just have to install it manually. 

The easiest way to do it is to just download the sMDT folder from the above github and just put it in the current working directory (same folder) of the code you're executing. A below example will show you how to import it, but it should just work if the sMDT *folder* is in the same folder as your code.

It's also possible to add it to the python path somehow, or move it to a location already on the path. That will be left as an excercise for the reader. 

Examples
--------
A very simple use case, such as at the tension station.
```python
from sMDT import db,tube                                #import the tube and db modules
from sMDT.data import tension                           #import the tension module
tubes = db.db()                                         #instantiate the database
tube1 = tube.Tube()                                     #make a new tube
tube1.tension.add_record(tension.TensionRecord(350))    #Store our new data in the tube, in the form of a TensionRecord object. 
tubes.add_tube(tube1)                                   #Store the tube in the database
```

Contribute
----------

- Issue Tracker: https://github.com/dravinflores/smdt/issues
- Source Code: https://github.com/dravinflores/smdt

Support
-------

If you are having issues, please let us know.
Talk to Paul or Dravin, or write an issue and put it in the issue tracker
