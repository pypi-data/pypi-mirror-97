"""
Created on Mar 03, 2021

@author: Siro

"""

from atframework.web.common.model.model import Model


class BoHelpdesk(Model):
    """
    Inherit the basic GUI action, and expand some methods on BO helpdesk
    """

    def open_helpdesk_page(self, css_selector):
        self._click_link_by_css(css_selector)
