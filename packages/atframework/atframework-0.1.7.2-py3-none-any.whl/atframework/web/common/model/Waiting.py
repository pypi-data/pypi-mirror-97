from atframework.web.common.model.Model import Model
from atframework.web.common.selenium.Seleniumhq301 import Seleniumhq301


class Waiting(Model):

    '''
    Inherit the basic GUI action, and expand waiting methods
    '''
    def refreshPage(self):
        self._refreshpage()

    def waits(self, wait_seonds):
        self._pause(wait_seonds)

    def waitCSSShown(self, css_selector):
        self._waitForCSSShownAndSleep(css_selector)

    def waitXpathShown(self, xpath):
        self._waitForXpathShownAndSleep(xpath)

    def waitXpathShown2(self, xpath):
        return self._waitForXpathShown2AndSleep(xpath)

    def waitCSSAndClick(self, css_selector):
        self._waitForCssShownAndClick(css_selector)



