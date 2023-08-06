'''
Created on Mar 03, 2021

@author: Siro

'''

import random
import datetime
import re
from atframework.web.utils.properties import Properties


class Utils(object):

    site = ""
    '''
    Get Random phone number from 100000-99999999999
    '''
    def get_phone_number(self):
        number = random.randint(100000, 99999999999)
        phoneNumber = str(number)
        return phoneNumber

    '''
    Get Random number from 1-10000
    '''

    def get_test_user_name(self):
        # a-z
        name1 = chr(random.randint(97, 122))
        name2 = chr(random.randint(97, 122))
        name3 = chr(random.randint(97, 122))
        number = random.randint(0, 100000)
        #abc98656
        username = str(name1) + str(name2) + str(name3) + str(number)
        return username

    def get_test_user_name_prefix(self, randint=random.randint(0, 10)):
        # a-z
        name1 = chr(random.randint(97, 122))
        name2 = chr(random.randint(97, 122))
        name3 = chr(random.randint(97, 122))
        number = randint
        #abc9
        usernamePrefix = str(name1) + str(name2) + str(name3) + str(number)
        return usernamePrefix

    def get_all_properties(self, properties_path):
        dictProperties = Properties(properties_path).getProperties()
        return dictProperties

    def get_setup_info(self, properties_path):
        dictInfos = Properties(properties_path).getProperties()
        return dictInfos