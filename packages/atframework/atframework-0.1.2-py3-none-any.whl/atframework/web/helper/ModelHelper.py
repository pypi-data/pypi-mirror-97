
from framework.web.common.model.Closing import Closing
from framework.web.common.model.Opening import Opening
from framework.web.common.model.Waiting import Waiting
from framework.web.common.model.BoLogin import BoLogin


class ModelHelper(Closing,Opening,Waiting,BoLogin):
    '''
    Integrate all model to this class, Use this class to drive test steps
    '''
