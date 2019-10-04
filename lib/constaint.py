from enum import Enum

class SettingDSAttr(Enum):
    USERONE = 'User name 1'
    USERTWO = 'User name 2'
    NAME = 'Setting name'
    LEVEL = 'Setting level'
    PROJECTONE = 'Project1'
    PROJECTTWO = 'Project2'
    SOURCE = 'Setting source'
    SEVERNAMEONE = 'Server name 1'
    SERVERNAMETWO = 'Server name 2'
    PARENTONE = 'First level group '
    PARENTTWO = 'Second level group'
    LOCATION = 'Setting location'
    ROWID = 'Order id'
    VALUEONE = 'Server 1 value'
    VALUETWO = 'Server 2 value'
    DIFFERENCE = 'Is different'

class SettingAttr(Enum):
    NAME = 'name'
    VALUE = 'value'
    LEVEL = 'level'
    PARENTONE = 'parent1'
    PARENTTWO = 'parent2'
    ID = 'row id'
    TYPE = 'type'
    SOURCE = 'source'
    LOCATION = 'location'
    HASHKEY = 'hashkey'
    RAWKEY = 'rawkey'

class ServerAttr(Enum):
    NAME = 'sn'
    PROJECT = 'pr'
    USER = 'usr'
    SOURCE = 'src'

