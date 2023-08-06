'''
Created on Mar 03, 2021

@author: Siro

'''

from atframework.web.common.model.closing import Closing
from atframework.web.common.model.opening import Opening
from atframework.web.common.model.waiting import Waiting
from atframework.web.common.model.bo_login import BoLogin
from atframework.web.common.model.bo_helpdesk import BoHelpdesk


class ModelHelper(Closing, Opening, Waiting, BoLogin, BoHelpdesk):
    '''
    Integrate all model to this class, Use this class to drive test steps
    '''
