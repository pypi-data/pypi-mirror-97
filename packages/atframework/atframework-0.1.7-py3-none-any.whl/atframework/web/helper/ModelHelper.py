
from atframework.web.common.model.Closing import Closing
from atframework.web.common.model.Opening import Opening
from atframework.web.common.model.Waiting import Waiting
from atframework.web.common.model.BoLogin import BoLogin


class ModelHelper(Closing,Opening,Waiting,BoLogin):
    '''
    Integrate all model to this class, Use this class to drive test steps
    '''
