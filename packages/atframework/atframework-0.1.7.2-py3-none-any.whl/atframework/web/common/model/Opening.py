
from atframework.web.common.model.Model import Model

class Opening(Model):

    def setupBrowser(self, browser_name):
        return self._openBrowser(browser_name)

    def maxBrowser(self):
        self._maxBrowser()

    def accessWebportal(self, site_name):
        self._accessWebSite(site_name)

    def accessWebportalTillOneTime(self, site_name):
        self._accessWebSiteTillOneTime(site_name)

    def bringToFront(self):
        self._bringToFront()
