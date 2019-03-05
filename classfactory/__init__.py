##############################
# ClassFactory main file
##############################
import classfactory.entities
from classfactory.config import VERSION


class Factory:

    version = VERSION

    Class = entities.Class
    Method = entities.Method
    Property = entities.Property
