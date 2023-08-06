import random
import datetime
import re
from atframework.web.utils.Properties import Properties


class Utils(object):

    site = ""

    '''
    Get Random phone number from 100000-99999999999
    '''

    def getPhoneNumber(self):
        number = random.randint(100000, 99999999999)
        phoneNumber = str(number)
        return phoneNumber

    '''
    Get Random number from 1-10000
    '''
    def getTestUserName(self):
        # a-z
        name1 = chr(random.randint(97, 122))
        name2 = chr(random.randint(97, 122))
        name3 = chr(random.randint(97, 122))
        number = random.randint(0, 100000)
        #abc98656
        username = str(name1) + str(name2) + str(name3) + str(number)
        return username

    def getTestUserNamePrefix(self):
        # a-z
        name1 = chr(random.randint(97, 122))
        name2 = chr(random.randint(97, 122))
        name3 = chr(random.randint(97, 122))
        number = random.randint(0, 10)
        #abc9
        usernamePrefix = str(name1) + str(name2) + str(name3) + str(number)
        return usernamePrefix

    def getAllProperties(self,properties_path):
        dictProperties = Properties(properties_path).getProperties()
        return dictProperties

    def getSetupInfo(self,properties_path):
        dictInfos = Properties(properties_path).getProperties()
        return dictInfos