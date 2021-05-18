    ###############################################################################
#   File: db.py
#   Author(s): Paul Johnecheck
#   Date Created: 11 April, 2021
#
#   Purpose: This is the class representing the database.
#    It will act as the main interface for reading and writing to the database. 
#
#   Known Issues:
#
#   Workarounds:
#
###############################################################################


# Import Preparation block.
# Currently only needed so the records in the mains work with the current imports.
import os
from sMDT.data.swage import SwageRecord
import sys

# Gets the path of the current file being executed.
path = os.path.realpath(__file__)
current_folder = os.path.dirname(os.path.abspath(__file__))
new_data_folder = os.path.join(current_folder, "new_data")
# Adds the folder that file is in to the system path

sys.path.append(current_folder)

from tube import Tube
from data.dark_current import DarkCurrent, DarkCurrentRecord
from data.station import *
import locks
import shelve
import pickle
import time
import datetime
import random
import re

class db:
    def __init__(self, path="database.s"):
        '''
        Constructor, builds the database object. Gets the path to the database
        '''
        self.path = path
        
    def size(self):
        '''
        Return the integer size of the database. May wait for the database to be unlocked
        '''
        db_lock = locks.Lock("database")
        db_lock.wait()
        tubes = shelve.open(self.path)
        ret_size = len(tubes)
        tubes.close()
        return ret_size
        
       
    def add_tube(self, tube: Tube()):
        '''
        Adds tube to the database. It does so by pickling the tube,
        and adding it to the new_data file for the database manager to add to the database with update()
        '''
        
        dt = datetime.datetime.now()
        timestamp = dt.timestamp()

        filename = str(timestamp) + str(random.randrange(0,999)) + ".p"

        if not os.path.isdir(new_data_folder):
            os.mkdir(new_data_folder)

        with open(os.path.join(new_data_folder, filename),"wb") as f:
            pickle.dump(tube, f)

    def get_tube(self, id):
        '''
        Returns the tube specified by id. May wait for the database to be unlocked.
        '''
        db_lock = locks.Lock("database")
        db_lock.wait()
        tubes = shelve.open(self.path)
        try:
            ret_tube = tubes[id]
        except KeyError:
            tubes.close()
            raise KeyError
        tubes.close()
        return ret_tube

    


#This object will eventually be moved to the legacy class.
class station_pickler:
    '''
    This class is designed to facilitate the interface between the database manager and the data generated by the stations. 
    This class will take whatever data is generated in the form of a csv file, and will read it into a sMDT tube object. 
    It will then pickle the object into the standard specified for new data for the db manager.
    '''
    def __init__(self, path="database.s"):
        '''
        Constructor, builds the pickler object. Gets the path to the database
        '''
        self.path = path

    '''
    This will pickle every file that is in the specified directory swagerDirectory
    '''
    def pickle_swage(self, swagerDirectory):
        pass # for now so tests don't fail
        db_lock = locks.Lock("database")
        db_lock.lock()

        for filename in os.listdir(swagerDirectory):
            with open(filename) as file:
                for line in file.readlines():
                    line = line.split(',')
                    # Here are the different csv types, there have been 3 versions
                    # The currently used version that includes endplug type 'Protvino' or 'Munich'
                    if len(line) == 9:
                        barcode = line[0].replace('\r\n', '')
                        rawLength = line[1]
                        swageLength = line[2]
                        sDate = line[3]
                        cCode = line[4]
                        eCode = line[5]
                        comment = line[6]
                        user    = line[7].replace('\r\n', '')
                        endplug_type = line[8]  # Not stored currently
                    # An earlier version when endplug type wasn't recorded
                    elif len(line) == 8:
                        barcode = line[0].replace('\r\n', '')
                        rawLength = line[1]
                        swageLength = line[2]
                        sDate = line[3]
                        cCode = line[4]
                        eCode = line[5]
                        comment = line[6]
                        user    = line[7].replace('\r\n', '')
                    # This was the very first iteration where there were only 3 things recorded
                    else:
                        barcode = line[0].replace('\r\n', '')
                        comment = line[1]
                        user    = line[2].replace('\r\n', '')
                        rawLength = "Unknown"
                        swageLength = "Unknown"                        
                        eCode = "Unknown"
                        cCode = "Unknown"
                        # Swager date was stored in the filename in this version
                        sDate = datetime.string_to_datetime(filename, '%m.%d.%Y_%H_%M_%S.csv')

                    tube = Tube()
                    tube.m_tube_id = barcode
                    tube.swage.m_user.append(user)
                    tube.new_comment(comment)
                    tube.swage.add_record(SwageRecord(raw_length=rawLength, swage_length=swageLength,
                                                          clean_code=cCode, error_code=eCode, date=sDate))
                    with open(os.path.join(new_data_folder, filename),"wb") as f: #FIXME
                        pickle.dump(tube, f)

        db_lock.unlock()

    def pickle_tension(self):
        pass
    def pickle_leak(self):
        pass
    def pickle_darkcurrent(self):
        pass




class db_manager():
    def __init__(self, path="database.s"):
        '''
        Constructor, builds the database manager object. Gets the path to the database
        '''
        self.path = path

    def wipe(self, confirm=False):
        '''
        Wipes the database. confirm must be "confirm" to proceed. 
        Excercise extreme caution with this, but it is necessary for many test cases.
        '''
        if confirm == 'confirm':
            db_lock = locks.Lock("database")
            db_lock.lock()

            tubes = shelve.open(self.path)
            for key in tubes:
                del tubes[key]

            tubes.close()

            db_lock.unlock()

    def update(self):
        '''
        Updates the database by looking for .p files in the new_data directory.
        They should be pickled tubes, and they will be added to the database
        Needs to be ran after a db object calls add_tube(), otherwise the database will not contain the data in time for get_tube()
        '''

        

        pickler = station_pickler()
        pickler.pickle_swage()
        pickler.pickle_tension()
        pickler.pickle_leak()
        pickler.pickle_darkcurrent()



        #Lock the database
        db_lock = locks.Lock("database")
        db_lock.lock()

        tubes = shelve.open(self.path)

        for filename in os.listdir(new_data_folder): 
            if filename.endswith(".p"):
                new_data_file = open(os.path.join(new_data_folder, filename), 'rb') #open the file
                tube = pickle.load(new_data_file)                                   #load the tube from pickle
                new_data_file.close()                                               #close the file
                if tube.getID() in tubes:                                           #add the tubes to the database
                    temp = tubes[tube.getID()] + tube                           
                    tubes[tube.getID()] = temp                          
                else:
                    tubes[tube.getID()] = tube
                os.remove(os.path.join(new_data_folder, filename))                 #delete the file that we added the tube from

        #close the database
        tubes.close()

        #unlock the database
        db_lock.unlock()
        

if __name__ == "__main__":
    new_data_folder = current_folder + "/new_data/"
    for filename in os.listdir(new_data_folder):
        new_data_file = open(new_data_folder + filename, 'r')
        new_data_file.close()
        