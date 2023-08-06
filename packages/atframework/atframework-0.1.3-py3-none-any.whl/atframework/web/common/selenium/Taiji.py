'''
Created on Mar 02, 2021

@author: Siro

'''

class Taiji(object):

    '''
    Open browser
    '''
    def _openBrowser(self, browser_name):
        assert False, 'action must be defined!'

    '''
    Close browser
    '''
    def _closeBrowser(self):
        assert False, 'action must be defined!'

    '''
    Finally: max browser
    '''
    def _maxBrowser(self):
        assert False, 'action must be defined!'

    '''
    Finally: bring the browser to front
    '''
    def _bringToFront(self):
        assert False, 'action must be defined!'

    '''
    access website
    '''
    def _accessWebSite(self, site_address):
        assert False, 'action must be defined!'

    '''
    find Specific Link By Class
    '''
    def _findLinkByClass(self, class_name):
        assert False, 'action must be defined!'

    '''
    click Specific Link By Class
    '''
    def _clickLinkByClass(self, class_name):
        assert False, 'action must be defined!'

    '''
    find Specific Link By id
    '''
    def _findLinkById(self, link_id):
        assert False, 'action must be defined!'

    '''
    click Specific Link By Class
    '''
    def _clickLinkById(self, link_id):
        assert False, 'action must be defined!'

    '''
    find Specific link By Text
    '''
    def _findLinkByText(self, link_text):
        assert False, 'action must be defined!'

    '''
    click Specific link By Text
    '''
    def _clickLinkByText(self, link_text):
        assert False, 'action must be defined!'

    '''
    click Specific link By xpath
    @param element - xpath
    '''
    def _clickLinkByXPath(self, xpath):
        assert False, 'action must be defined!'

    '''
    find Specific Button By css_selector
    param element - css_selector
    '''
    def _findLinkByCSS(self, css_selector):
        assert False, 'action must be defined!'


    '''
    find Specific Link By xpath
    '''
    def _findLinkByXPath(self, xpath):
        assert False, 'action must be defined!'

    '''
    click Specific Button By css_selector
    param element - css_selector
    '''
    def _clickLinkByCSS(self, css_selector):
        assert False, 'action must be defined!'

    '''
    find Text Field By Id 
    '''
    def _findTextFieldById(self, field_id):
        assert False, 'action must be defined!'

    '''
    click Text Field By Id
    '''
    def _typeInTextFieldById(self, field_id, input_text):
        assert False, 'action must be defined!'


    '''
    click Text Field By CSS
    '''
    def _typeInTextFieldByCSS(self, field_id, input_text):
        assert False, 'action must be defined!'

    '''
    click Text Field By XPath
    '''
    def _typeInTextFieldByXPath(self, field_xpath, input_text):
        assert False, 'action must be defined!'


    '''
    click Text Field By XPath and click Enter on keyborad
    '''
    def _typeInTextFieldByXPathAndClickEnter(self, field_xpath, input_text):
        assert False, 'action must be defined!'

    '''
    find Specific Button By Class
    '''
    def _findButtonByClass(self, class_name):
        assert False, 'action must be defined!'

    '''
    find Specific Button By Id
    '''
    def _findButtonById(self, id_name):
        assert False, 'action must be defined!'

    '''
    click Specific Button By Class
    '''
    def _clickButtonByClass(self, class_name):
        assert False, 'action must be defined!'

    '''
    click Specific Button By id
    param element - class_name
    '''
    def _clickButtonById(self, id_name):
        assert False, 'action must be defined!'

    '''
    click Specific Button By CSS
    @param element - css_selector
    '''
    def _clickButtonByCSS(self, css_selector):
        assert False, 'action must be defined!'

    '''
    click Specific Button By CSS and javascript
    @param element - css_selector
    '''
    def _clickElementByLocatorScript(self,css_selector):
        assert False, 'action must be defined!'

    '''
    click Specific Button By xpath and javascript
    @param element - xpath
    '''
    def _clickElementByLocatorScriptAndXPath(self,xpath):
        assert False, 'action must be defined!'

    '''
    If there are some same element on the page, click Specific Button By index and javascript (index start form 1)
    @param element - css_selector
    '''
    def _clickButtonInListByLocatorScript(self, css_selector, index):
        assert False, 'action must be defined!'

    '''
    Click Element By Locator
    @param element - text, locator
    '''
    def _clickElementByLocator(self, css_selector):
        assert False, 'action must be defined!'

    '''
    Click Element By XPath
    @param element - text, XPath
    '''
    def _clickElementByXPath(self, xpath):
        assert False, 'action must be defined!'

    '''
    Find Element By Locator
    @param element - text, locator
    '''
    def _findElementByLocator(self, css_selector):
        assert False, 'action must be defined!'

    '''
    Double click on element
    @param - element
    '''
    def doubleClickElement(self,webElement):
        assert False, 'action must be defined!'


    '''
    Double click element by Id
    @param - elementId
    '''
    def doubleClickElementById(self, elementId):
        assert False, 'action must be defined!'

    '''
    Double click element by Id
    @param - locator
    '''
    def doubleClickElementByCss(self, locator):
        assert False, 'action must be defined!'

    '''
    switch to alert
    @param - 
    '''
    def _switchToAlert(self):
        assert False, 'action must be defined!'


    '''
    switch and then close the alert
    @param - 
    '''
    def _switchAndCloseAlert(self):
        assert False, 'action must be defined!'

    '''
    Select Element in DropMenu
    @param element - locator, text, value
    '''
    def _selectDropDownMenuElementByLocator(self, css_selector, text, value):
        assert False, 'action must be defined!'

    '''
    Select Element in DropMenu
    @param element - xpath, text, value
    '''
    def _selectDropDownMenuElementByXpath(self, xpath, text, value):
        assert False, 'action must be defined!'

    '''
    Select Element by index in DropMenu
    @param element - locator, index
    '''
    def _selectDropDownMenuElementByIndex(self, css_selector, index):
        assert False, 'action must be defined!'


    '''
    Select Element by value in DropMenu
    @param element - locator, value
    '''
    def _selectDropDownMenuElementByValue(self, css_selector, value):
        assert False, 'action must be defined!'


    '''
    Select Element by text in DropMenu
    @param element - locator, text
    '''
    def _selectDropDownMenuElementByText(self, css_selector, text):
        assert False, 'action must be defined!'


    '''
    Return select options in DropMenu
    @param element - locator
    '''
    def _getSelectDropDownMenuOptions(self, css_selector):
        assert False, 'action must be defined!'

    '''
     is select check box or not
     @param element - xpath
     '''
    def _isSelectCheckBoxByXpath(self, xpath):
        assert False, 'action must be defined!'

    '''
    If there are some same element on the page, click Specific Button By index (index start form 0)
    @param element - css_selector
    '''
    def _clickButtonInList(self, css_selector, index):
        assert False, 'action must be defined!'

    '''
    If there are some same element on the page, click Specific Button By index (index start form 1)
    @param element - xpath
    '''
    def _clickButtonInListViaXPath(self, xpath, index):
        assert False, 'action must be defined!'

    '''
    click Specific Button By xpath
    @param element - xpath
    '''
    def _clickButtonByXPath(self, xpath):
        assert False, 'action must be defined!'

    '''
    Clear text by css_selector in text field
    @param element - locator
    '''
    def _clearTextFieldByCSS(self, css_selector):
        assert False, 'action must be defined!'

    '''
     Clear text by xpath in text field
     @param element - xpath
     '''
    def _clearTextFieldByXpath(self, xpath):
        assert False, 'action must be defined!'

    '''
     Clear text by xpath in text field and send Enter
     @param element - xpath
     '''
    def _clearTextFieldByXpathAndEnter(self, xpath):
        assert False, 'action must be defined!'

    '''
    Get Text By CSS
    @param element - css locator
    '''
    def _getTextByCSS(self, css_selector):
        assert False, 'action must be defined!'

    '''
    Get Text By XPath
    @param element - XPath
    '''
    def _getTextByXPath(self, xpath):
        assert False, 'action must be defined!'

    '''
    click center key By CSS
    @param element - css locator
    '''
    def _clickEnterKeyByCSS(self, css_selector):
        assert False, 'action must be defined!'

    '''
    If there are some same elements on the page, find whether has expected text on these elements.
    @param element - expected_text
    '''
    def _isExpectedTextInElements(self, expected_text):
        assert False, 'action must be defined!'

    '''
    Get Value By XPath
    @param element - XPath
    '''
    def _getValueByXPath(self, xpath):
        assert False, 'action must be defined!'

    '''
     Get input disable text By locator script
     @param element - css_selector
     '''
    def _getInputDisableTextByLocatorScript(self,css_selector):
        assert False, 'action must be defined!'

    '''
    switch the frame for locate elements.
    '''
    def _switchFrame(self):
        assert False, 'action must be defined!'

    '''
    switch the frame back to default.
    '''
    def _switchFrameBackToDefault(self):
        assert False, 'action must be defined!'

    '''
    refresh the current page.
    '''
    def _refreshpage(self):
        assert False, 'action must be defined!'

    '''
    Get elements's URL By Text
    @param element - link_text
    '''
    def _getElementURLByText(self, link_text):
        assert False, 'action must be defined!'

    '''
    Take screenshot as jpg and save file
    '''
    def _takeScreenshotAsFile(self, file_name):
        assert False, 'action must be defined!'