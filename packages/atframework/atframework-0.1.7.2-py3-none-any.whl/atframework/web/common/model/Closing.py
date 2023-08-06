from atframework.web.common.model.Model import Model


class Closing(Model):

    def tearDownBrowser(self):
        self._closeBrowser()

    def takeScreenshotFile(self, file_name):
        self._takeScreenshotAsFile(file_name)

    def clickLogoutButtonViaCSS(self, link_css):
        self._clickElementByLocator(link_css)

    def isLogoutSuccessfully(self, link_id):
        self._waitForIdShownAndSleep2s(id_name=link_id)
        return self._findLinkById(link_id)