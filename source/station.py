###############################################################################
#   File: station.py
#   Author(s): Dravin Flores
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

class Station:
    modes = [
        'first',
        'last',
        'mean',
        'mode'
    ]

    def __init__(self, users: [], tests: []):
        m_users = users
        m_tests = tests

    def __str__(self):
        raise NotImplementedError

    def __repr__(self):
        return self.__str__()

    def fail(self):
        raise NotImplementedError

    def get_users(self):
        return self.m_users

    def add_user(self, user):
        self.m_users.append(user)

    def get_test(self, mode = 'last'):
        pass

    def set_test(self, test: tuple):
        raise NotImplementedError
