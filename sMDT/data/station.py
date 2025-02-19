###############################################################################
#   File: station.py
#   Author(s): Dravin Flores, Paul Johnecheck
#   Date Created: 02 April, 2021
#
#   Purpose: This file houses the base class that all station classes will
#       inherit from.
#
#   Known Issues:
#
#   Workarounds:
#
###############################################################################

modes = {
    "last"  :  lambda station: station.m_records[-1],
    "first" :  lambda station: station.m_records[0],
    "all"   :  lambda station: station.m_records
    
}



# Import Preparation block.
# Currently only needed so the tests in the mains work with the current imports.
import os
import sys

# Gets the path of the current file being executed.
path = os.path.realpath(__file__)
current_folder = os.path.dirname(os.path.abspath(__file__))

# Adds the folder that file is in to the system path
sys.path.append(current_folder)


class Station:
    """
    Abstract class representing a station that will record data on a tube
    """
    def __init__(self):
        # WARNING
        # Initially, this init function and the inheriting station's functions
        # looked something like
        # def __init__(self, records=[])
        #   self.m_records = records
        # I don't know why, but this is apparently a terrible idea
        # that somehow makes the lists in every station object be the same
        # object and share their users and records. Again, no idea why, I
        # encountered the problem and traced it back here and found that
        # removing it fixed it
        self.m_records = []


    def __str__(self):
        raise NotImplementedError

    def __repr__(self):
        return self.__str__()

    def __add__(self, other):
        ret = type(self)()
        ret.m_records = self.m_records + other.m_records
        return ret

    def fail(self, mode='last'):
        if type(mode) == str:
            return modes[mode](self).fail()
        elif type(mode) == type(lambda x: x): #Annoying but necessary hack to check if it's a lambda.
            return mode(self).fail()
        else:
            raise RuntimeError()

    def get_record(self, mode='last'):
        """Given a selected mode, returns the respective record"""
        if type(mode) == str:
            return modes[mode](self)
        elif type(mode) == type(lambda x: x): #Annoying but necessary hack to check if it's a lambda.
            return mode(self)
        else:
            raise RuntimeError()

    def add_record(self, record):
        """Adds a record to the station's records"""
        self.m_records.append(record)



