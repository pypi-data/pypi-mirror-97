'''
Created on Mar 03, 2021

@author: Siro

'''

from atframework.web.common.maps.resource_maps import ResourceMaps
from atframework.web.common.maps.elements_maps import ElementsMaps
from atframework.web.helper.model_helper import ModelHelper
from atframework.tools.log.config import logger
from atframework.web.utils.utils import Utils
import pyautogui


class WebFlows(ModelHelper):
    '''
    Integrate all flows to this class, Use this class to drive test steps
    '''
    EM = ElementsMaps()
    RM = ResourceMaps()

    test_email = RM.TEST_EMAIL

    def open_browser(self):
        logger.info('[AtLog] ----- start to init browser driver')
        return self.setup_browser(self.RM.BROWSER_NAME)

    def bring_browser_to_front(self):
        logger.info('[AtLog] ----- bring the browser to front')
        self.bring_to_front()

    def close_browser(self):
        self.teardown_browser()

    def get_screenshot_file(self, file_name):
        self.take_screenshot_file(file_name)

    '''
    ----------BO------------
    '''

    def bo_login(self, site=RM.RUNNING_SITE):
        """
        login form bo.

        :param site: login site address
        :return: none
        """
        logger.info('[AtLog] ----- Access BO')
        self.open_web_portal(self.RM.BO_ADDRESS)
        logger.info('[AtLog] ----- Reload BO to find elements')
        self.open_web_portal(self.RM.BO_ADDRESS)
        logger.info('[AtLog] ----- Input admin')
        self.type_email_via_css(self.EM.bo_username_field_css,
                                self.RM.USERNAME_DEV_BO)
        logger.info('[AtLog] ----- Input password')
        self.type_password_via_css(self.EM.bo_password_field_css,
                                   self.RM.PASSWORD_DEV_BO)
        logger.info('[AtLog] ----- Click the login button on BO')
        self.click_login_button_via_css(self.EM.bo_login_button_css)
        logger.info('[AtLog] ----- check whether the site is selected on bo')
        if self.is_find_site_not_selected_via_css(self.EM.bo_site_not_select_text_css) is True:
            logger.info('[AtLog] ----- select site on BO')
            if site == 'dev':
                self.waits(2)
                logger.info('[AtLog] ----- click select site button')
                self.click_select_by_xpath(self.EM.bo_site_select_button_xpath)
                self.waits(2)
                logger.info('[AtLog] ----- select site is luckycasino BO')
                self.click_select_by_xpath(
                    self.EM.bo_site_select_luckycasino_xpath)
                self.waits(2)
            else:
                self.click_select_by_xpath(self.EM.bo_site_select_button_xpath)
                self.waits(2)
                self.click_select_by_xpath(
                    self.EM.bo_site_select_luckycasino_xpath)
                self.waits(2)
        else:
            logger.info('[AtLog] ----- the site is selected on BO')
            pass

    def bo_search_player(self, player_text, flag=0):
        """
        @precondition: the player is logged in on bo.
        This is search player from bo.

        :param player_text:
        :param flag: 0: input the search text and click enter in keyboard,
        1:input the search text, then click search button
        :return: whether search player successfully

        """
        logger.info('[AtLog] ----- Click the helpdesk link')
        self.open_helpdesk_page(self.EM.bo_helpdesk_link_css)
        self.waits(5)
        if flag == 0:
            logger.info('[AtLog] ----- input search text and press Enter button on keyboard')
            self.type_search_text_via_xpath_and_enter(self.EM.bo_search_text_field_xpath, player_text)
            self.waits(5)
        elif flag == 1:
            logger.info('[AtLog] ----- input search text')
            self.type_search_text_via_css(self.EM.bo_search_text_field_css, player_text)
            logger.info('[AtLog] ----- click search button')
            self.click_search_button_via_css(self.EM.bo_search_button_css)
        return self.is_searched_player_via_text(player_text)
        # logger.info('[AtLog] ----- open player details page')
        # self.click_searched_player_link_via_text(player_text)