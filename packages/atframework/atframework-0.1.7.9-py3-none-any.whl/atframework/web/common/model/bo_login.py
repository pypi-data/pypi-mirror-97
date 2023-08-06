"""
Created on Mar 03, 2021

@author: Siro

"""

from atframework.web.common.model.model import Model


class BoLogin(Model):
    """
    Inherit the basic GUI action, and expand Bo login methods
    """
    def open_web_portal(self, site_address):
        self._access_website_till_one_time(site_address)

    def type_email_via_css(self, field_css, input_text):
        self._type_in_text_field_by_css(field_css, input_text)

    def type_password_via_css(self, field_css, input_text):
        self._type_in_text_field_by_css(field_css, input_text)

    def click_login_button_via_css(self, link_css):
        self._click_element_by_locator(link_css)

    def is_find_site_not_selected_via_css(self, css_selector):
        return self._find_link_by_css(css_selector)

    def click_select_by_xpath(self, xpath):
        self._click_element_by_xpath(xpath)
