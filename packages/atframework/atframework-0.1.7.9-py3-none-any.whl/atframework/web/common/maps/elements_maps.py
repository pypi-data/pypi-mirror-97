"""
Created on Mar 04, 2021

@author: Siro

"""


class ElementsMaps(object):
    """
    store the web elements in this Class
    """
    protection_page_logo_xpath = "//*[@id='logo']/img"
    protection_username_css = "input[type='text'][id='username'][name='siteProtectionUsername']"
    protection_password_css = "input[id='password'][name='siteProtectionPassword'][type='password']"
    protection_login_css = "input[class='btn btn-primary'][value='Login'][title='Login'][type='submit']"
    """
    BO
    """
    bo_username_field_css = "input[id='login_username'][class='bo-field__control form-control bo-field__control--textfield validation-required']"
    bo_username_filed_xpath = "//*[@id='login_username']"
    bo_password_field_css = "input[id='login_password'][class='bo-field__control form-control bo-field__control--password validation-required']"
    bo_login_button_css = "button[id='login_0'][class='bo-button bo-button--primary bo-button--submit btn btn-primary']"
    bo_site_not_select_text_css = "button[class='bo-alert__close close'][data-dismiss='alert']"
    bo_site_select_button_xpath = "//*[@id='bo-page-dashboard-summary']/div/header/div/div/div[2]/div[4]/div/button"
    bo_site_select_luckycasino_xpath = "//*[@id='bo-page-dashboard-summary']/div/header/div/div/div[2]/div[4]/div/div/ul/li[4]/a"
    bo_helpdesk_link_css = "a[class='bo-nav__control'][href='playerSearch!view']"
    bo_search_text_field_css = "input[id='playerSearch_freeText'][class='bo-field__control form-control bo-field__control--textfield']"
    bo_search_text_field_xpath = "//*[@id='playerSearch_freeText']"

    bo_helpdesk_link_css = "a[class='bo-nav__control'][href='playerSearch!view']"
    bo_search_text_field_css = "input[id='playerSearch_freeText'][class='bo-field__control form-control bo-field__control--textfield']"
    bo_search_text_field_xpath = "//*[@id='playerSearch_freeText']"
    bo_search_button_css = "button[id='playerSearch_0'][class='bo-button bo-button--primary bo-button--submit btn btn-primary']"
    bo_user_xpath = ".//*[@id='players']/tbody/tr/td[3]/a"
    bo_account_status_selector_css = "select[id='player_user_userStatus'][class='bo-field__control form-control bo-field__control--select']"
    bo_account_status_selector_active_value = "active"
    bo_update_button_css = "button[id='player_0'][class='bo-button bo-button--primary bo-button--submit btn btn-primary'][type='submit']"
    bo_update_1st_button_xpath = ".//*[@id='player_0'][1]"
