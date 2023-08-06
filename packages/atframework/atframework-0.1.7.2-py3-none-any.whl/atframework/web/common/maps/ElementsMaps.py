
class ElementsMaps(object):
    '''
    store the web elements in this Class
    '''
    protection_page_logo_xpath = "//*[@id='logo']/img"
    protection_username_css = "input[type='text'][id='username'][name='siteProtectionUsername']"
    protection_password_css = "input[id='password'][name='siteProtectionPassword'][type='password']"
    protection_login_css = "input[class='btn btn-primary'][value='Login'][title='Login'][type='submit']"

    '''
    BO
    '''
    bo_username_field_css = "input[id='login_username'][class='bo-field__control form-control bo-field__control--textfield validation-required']"
    bo_username_filed_xpath = "//*[@id='login_username']"
    bo_password_field_css = "input[id='login_password'][class='bo-field__control form-control bo-field__control--password validation-required']"
    bo_login_button_css = "button[id='login_0'][class='bo-button bo-button--primary bo-button--submit btn btn-primary']"
    bo_site_not_select_text_css = "button[class='bo-alert__close close'][data-dismiss='alert']"
    bo_site_select_button_xpath = "//*[@id='bo-page-dashboard-summary']/div/header/div/div/div[2]/div[4]/div/button"
    bo_site_select_luckycasino_xpath = "//*[@id='bo-page-dashboard-summary']/div/header/div/div/div[2]/div[4]/div/div/ul/li[4]/a"