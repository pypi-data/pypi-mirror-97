"""
Created on Mar 04, 2021

@author: Siro

"""

import os
import platform
import sys
from atframework.web.utils.utils import Utils


class ResourceMaps(object):
    UT = Utils()
    setupPropertiesPath = os.path.abspath(os.path.dirname(
        os.getcwd())) + "/properties/setup.properties"
    setupInfo = UT.get_setup_info(setupPropertiesPath)
    documentImagePath = os.path.abspath(os.path.dirname(
        os.getcwd())) + '/atframework/web/common/images/testDocument.jpg'

    '''
    site setup info
    '''
    BROWSER_NAME = setupInfo['browserName']
    RUNNING_SITE = setupInfo['site']
    if Utils.site == "":
        running_site = RUNNING_SITE
    else:
        running_site = str(Utils.site)

    propertiesPath = os.path.abspath(os.path.dirname(os.getcwd(
    ))) + "/properties/" + running_site + "/integration.properties"
    dicProperties = UT.get_all_properties(propertiesPath)

    '''
    site protection info
    '''
    PROTECTION_USERNAME = dicProperties['protectionUsername']
    PROTECTION_PASSWORD = dicProperties['protectionPassword']

    '''
    the following are web site links
    '''
    SITE_ADDRESS = dicProperties['siteProtal']
    SITE_ADDRESS_EN = dicProperties['siteProtalEN']

    '''
    the following are Dev BO links
    '''
    BO_ADDRESS = dicProperties['boProtal']

    '''
    the following are Dev BO Admin account info
    '''
    USERNAME_DEV_BO = dicProperties['usernameBo']
    PASSWORD_DEV_BO = dicProperties['passwordBo']

    '''
    the following test account info should be changed before testing
    '''
    TEST_EMAIL = UT.get_test_user_name() + "@test.com"
    TEST_EMAIL_PREFIX = UT.get_test_user_name_prefix()
    TEST_NICKNAME = UT.get_test_user_name()
    TEST_PASSWORD = dicProperties['testPasswrod']

    # '''
    # set the current browser
    # '''
    # BROWSER_NAME = dicProperties['browserName']

    '''
    profile page
    '''
    STREET_NUMBER = dicProperties['streetNumber']
    HOUSE_NUMBER = dicProperties['houseNumber']
    DISTRICT = dicProperties['district']
    CITY = dicProperties['city']
    ZIP_CODE = dicProperties['zipCode']
    PHONE_NUMBER = UT.get_phone_number()
    BIRTH_DAY = dicProperties['birthday']
    BIRTH_MONTH = dicProperties['birthmonth']
    BIRTH_MONTH_ENGLISH = dicProperties['birthmonthEnglish']
    BIRTH_YEAR = dicProperties['birthyear']
    DOCUMENT_NAME = dicProperties['documentName']
    DOCUMENT_IMAGE_PATH = documentImagePath

    '''
    testing account
    '''
    USERID = dicProperties['userid']
    USER_EMAIL = dicProperties['userEmail']
