'''
Created on Mar 03, 2021

@author: Siro

'''

from atframework.web.common.maps.resource_maps import ResourceMaps
from atframework.web.common.maps.elements_maps import ElementsMaps
from atframework.web.helper.model_helper import ModelHelper
from atframework.tools.log.config import logger
from atframework.web.utils.Utils import Utils
import pyautogui


class WebFlows(ModelHelper):
    '''
    Integrate all flows to this class, Use this class to drive test steps
    '''
    MH = ModelHelper()
    EM = ElementsMaps()
    RM = ResourceMaps()

    test_email = RM.TEST_EMAIL

    def openBrowser(self):
        logger.info('[AtLog] ----- start to init browser driver')
        return self.MH.setup_browser(self.RM.BROWSER_NAME)

    def bring2Front(self):
        logger.info('[AtLog] ----- bring the browser to front')
        self.MH.bring_to_front()

    def closeBrowser(self):
        self.MH.teardown_browser()

    def getScreenshotFile(self, file_name):
        self.MH.take_screenshot_file(file_name)

    '''
    ----------BO------------
    '''

    def boLogin(self, site=RM.RUNNING_SITE):
        logger.info('[AtLog] ----- Access BO')
        self.MH.open_web_portal(self.RM.BO_ADDRESS)
        logger.info('[AtLog] ----- Reload BO to find elements')
        self.MH.open_web_portal(self.RM.BO_ADDRESS)
        logger.info('[AtLog] ----- Input admin')
        self.MH.type_email_via_css(self.EM.bo_username_field_css,
                                   self.RM.USERNAME_DEV_BO)
        logger.info('[AtLog] ----- Input password')
        self.MH.type_password_via_css(self.EM.bo_password_field_css,
                                      self.RM.PASSWORD_DEV_BO)
        logger.info('[AtLog] ----- Click the login button on BO')
        self.MH.click_login_button_via_css(self.EM.bo_login_button_css)
        logger.info('[AtLog] ----- check whether the site is selected on bo')
        if self.MH.is_find_site_not_selected_via_css(self.EM.bo_site_not_select_text_css) is True:
            logger.info('[AtLog] ----- select site on BO')
            if site == 'dev':
                self.MH.waits(2)
                logger.info('[AtLog] ----- click select site button')
                # self.MH.selectDropDownMenuViaXpathValue(self.EM.bo_site_select_xpath, self.EM.bo_site_select_value)
                self.MH.click_select_by_xpath(self.EM.bo_site_select_button_xpath)
                self.MH.waits(2)
                logger.info('[AtLog] ----- select site is luckycasino BO')
                self.MH.click_select_by_xpath(
                    self.EM.bo_site_select_luckycasino_xpath)
                self.MH.waits(2)
            else:
                # self.MH.selectDropdownMenu(self.EM.bo_site_select_css, self.EM.bo_site_select_text, self.EM.bo_site_select_value)
                self.MH.click_select_by_xpath(self.EM.bo_site_select_button_xpath)
                self.MH.waits(2)
                self.MH.click_select_by_xpath(
                    self.EM.bo_site_select_luckycasino_xpath)
                self.MH.waits(2)
        else:
            logger.info('[AtLog] ----- the site is selected on BO')
            pass
