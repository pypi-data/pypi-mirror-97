
from atframework.web.common.model.Model import Model

class BoLogin(Model):
    '''
    Inherit the basic GUI action, and expand some login methods
    '''

    def openWebProtal(self, site_address):
        self._accessWebSiteTillOneTime(site_address)

    def typeEmailViaCSS(self, field_css, input_text):
        self._typeInTextFieldByCSS(field_css, input_text)

    def typePasswordViaCSS(self, field_css, input_text):
        self._typeInTextFieldByCSS(field_css, input_text)

    def clickLoginButtonViaCSS(self, link_css):
        self._clickElementByLocator(link_css)

    def isFindSiteNotSelectedViaCSS(self, css_selector):
        return self._findLinkByCSS(css_selector)

    def clickSelectByXpath(self, xpath):
        self._clickElementByXPath(xpath)