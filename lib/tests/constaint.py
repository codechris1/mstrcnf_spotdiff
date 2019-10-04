from enum import Enum

class SettingDSAttr(Enum):
    USERONE = 'usr1'
    USERTWO = 'usr2'
    NAME = 'setname'
    LEVEL = 'setlevel'
    PROJECTONE = 'pr1'
    PROJECTTWO = 'pr2'
    SOURCE = 'source'
    SEVERNAMEONE = 'sn1'
    SERVERNAMETWO = 'sn2'
    PARENTONE = 'parent1'
    PARENTTWO = 'parent2'
    ROWID = 'row id'
    VALUEONE = 'value1'
    VALUETWO = 'value2'
    DIFFERENCE = 'diff'

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

