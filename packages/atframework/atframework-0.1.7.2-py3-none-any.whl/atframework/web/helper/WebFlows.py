from atframework.web.common.maps.ResourceMaps import ResourceMaps
from atframework.web.common.maps.ElementsMaps import ElementsMaps
from atframework.web.helper.ModelHelper import ModelHelper
# from resources.log.config import logger
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
        return self.MH.setupBrowser(self.RM.BROWSER_NAME)

    def bring2Front(self):
        logger.info('[AtLog] ----- bring the browser to front')
        self.MH.bringToFront()

    def closeBrowser(self):
        self.MH.tearDownBrowser()

    def getScreenshotFile(self, file_name):
        self.MH.takeScreenshotFile(file_name)


    '''
    ----------BO------------
    '''
    def boLogin(self, site=RM.RUNNING_SITE):
        logger.info('[AtLog] ----- Access BO')
        self.MH.openWebProtal(self.RM.BO_ADDRESS)
        logger.info('[AtLog] ----- Reload BO to find elements')
        self.MH.openWebProtal(self.RM.BO_ADDRESS)
        logger.info('[AtLog] ----- Input admin')
        self.MH.typeEmailViaCSS(self.EM.bo_username_field_css, self.RM.USERNAME_DEV_BO)
        logger.info('[AtLog] ----- Input password')
        self.MH.typePasswordViaCSS(self.EM.bo_password_field_css, self.RM.PASSWORD_DEV_BO)
        logger.info('[AtLog] ----- Click the login button on BO')
        self.MH.clickLoginButtonViaCSS(self.EM.bo_login_button_css)
        logger.info('[AtLog] ----- check whether the site is selected on bo')
        if self.MH.isFindSiteNotSelectedViaCSS(self.EM.bo_site_not_select_text_css) is True:
            logger.info('[AtLog] ----- select site on BO')
            if site == 'dev':
                self.MH.waits(2)
                logger.info('[AtLog] ----- click select site button')
                #self.MH.selectDropDownMenuViaXpathValue(self.EM.bo_site_select_xpath, self.EM.bo_site_select_value)
                self.MH.clickSelectByXpath(self.EM.bo_site_select_button_xpath)
                self.MH.waits(2)
                logger.info('[AtLog] ----- select site is luckycasino BO')
                self.MH.clickSelectByXpath(self.EM.bo_site_select_luckycasino_xpath)
                self.MH.waits(2)
            else:
                #self.MH.selectDropdownMenu(self.EM.bo_site_select_css, self.EM.bo_site_select_text, self.EM.bo_site_select_value)
                self.MH.clickSelectByXpath(self.EM.bo_site_select_button_xpath)
                self.MH.waits(2)
                self.MH.clickSelectByXpath(self.EM.bo_site_select_luckycasino_xpath)
                self.MH.waits(2)
        else:
            logger.info('[AtLog] ----- the site is selected on BO')
            pass