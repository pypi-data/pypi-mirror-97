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

    def type_search_text_via_css(self, field_css, input_text):
        self._type_in_text_field_by_css(field_css, input_text)

    def type_search_text_via_xpath(self, field_xpath, input_text):
        self._type_in_text_field_by_xpath(field_xpath, input_text)

    def type_search_text_via_xpath_and_enter(self, field_xpath, input_text):
        self._type_in_text_field_by_xpath_and_click_enter(field_xpath, input_text)

    def is_searched_player_via_text(self, text):
        return self._find_link_by_text(text)

    def click_search_button_via_css(self, css_selector):
        self._click_link_by_css(css_selector)
