
from atframework.web.common.model.Model import Model

class BoHelpdesk(Model):
    '''
    Inherit the basic GUI action, and expand some methods on BO helpdesk
    '''

    def openHelpdeskPage(self, css_selector):
        self._clickLinkByCSS(css_selector)
