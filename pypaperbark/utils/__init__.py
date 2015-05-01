# -*- coding: utf-8 -*-

class ZFSError(Exception):
    '''
    zfs error
    '''
    def __init__(self,err_str):
        self.__error_msg = err_str
    def __str__(self):
        return str(self.__error_msg)

